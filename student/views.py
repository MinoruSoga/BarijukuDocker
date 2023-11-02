from django.shortcuts import render, redirect
from django.views.generic import (
    DetailView,
    FormView,
    ListView,
    TemplateView,
    View,
    CreateView,
)
import datetime
from django.conf import settings
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone

# from django.contrib.auth.models import User
from app.models import (
    Calendar,
    Prefecture,
    City,
    MeetingSchedule,
    ChatGPTLog,
    CouponStudent,
    Coupon,
    CouponStudent,
)
from .models import (
    AtamaPlus,
    StudySapuri,
    Student,
    School,
    ClubActivity,
    TestCategory,
    Subject,
    TestResult,
)
import math
from .forms import AtamaPlusForm, StudySapuriForm, StudentProfielForm
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
import stripe as stp
from app.utils.stripe import Stripe
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from dateutil.relativedelta import relativedelta
import requests
import openai
import deepl
from django.contrib.auth import get_user_model

User = get_user_model()


class IndexView(TemplateView):
    template_name = "student/index.html"

    def get(self, request, *args, **kwargs):
        try:
            atama_plus = AtamaPlus.objects.get(user=self.request.user.id)
        except:
            atama_plus = None
        try:
            study_sapuri = StudySapuri.objects.get(user=self.request.user.id)
        except:
            study_sapuri = None
        try:
            meeting_schedules = MeetingSchedule.objects.filter(
                student=Student.objects.get(user=self.request.user.id),
                start_date__gt=timezone.now(),
            )
        except:
            meeting_schedules = None
        try:
            calendars = Calendar.objects.filter(
                user=self.request.user.id, start_date__gt=timezone.now()
            )
        except:
            calendars = None
        return render(
            request,
            self.template_name,
            {
                "atama_plus": atama_plus,
                "study_sapuri": study_sapuri,
                "meeting_schedules": meeting_schedules,
                "calendars": calendars,
            },
        )


class CalendarView(TemplateView):
    template_name = "student/calendar.html"
    error_message = "正しくない時間が入力されていたため、登録されませんでした。"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # staff = get_object_or_404(Staff, pk=self.kwargs['pk'])
        today = datetime.date.today()
        selected_today = datetime.date.today().strftime("%Y-%m-%d")

        # どの日を基準にカレンダーを表示するかの処理。
        # 年月日の指定があればそれを、なければ今日からの表示。
        year = self.kwargs.get("year")
        month = self.kwargs.get("month")
        day = self.kwargs.get("day")
        if year and month and day:
            base_date = datetime.date(year=year, month=month, day=day)
        else:
            base_date = today

        # カレンダーは1週間分表示するので、基準日から1週間の日付を作成しておく
        days = [base_date + datetime.timedelta(days=day) for day in range(7)]
        start_day = days[0]
        end_day = days[-1]

        # 10時から23時まで1時間刻み、1週間分の、値がTrueなカレンダーを作る
        calendar = {}
        for hour in settings.DAILY_SCHEDULE:
            row = {}
            for day in days:
                # row[day] = True
                row[day] = False
            calendar[hour] = row

        # カレンダー表示する最初と最後の日時の間にある予約を取得する
        start_time = datetime.datetime.combine(
            start_day, datetime.time(hour=10, minute=0, second=0)
        )
        end_time = datetime.datetime.combine(
            end_day, datetime.time(hour=23, minute=0, second=0)
        )

        for schedule in Calendar.objects.filter(user=self.request.user.id).exclude(
            Q(start_date__gt=end_time) | Q(end_date__lt=start_time)
        ):
            start_dt = timezone.localtime(schedule.start_date)
            end_dt = timezone.localtime(schedule.end_date)
            end_dt = end_dt + datetime.timedelta(minutes=-30)
            booking_date = start_dt.date()
            # booking_hour = str(start_dt.hour) + ":" + str(start_dt.strftime("%M"))
            start_time = str(start_dt.strftime("%H:%M"))
            end_time = str(end_dt.strftime("%H:%M"))
            if start_time in calendar and booking_date in calendar[start_time]:
                target_time = start_time
                # calendar[start_time][booking_date] = False
                calendar[start_time][booking_date] = schedule.pk
                i = 0
                while i < 20:
                    i += 1
                    target_time_array = target_time.split(":")
                    start_min = int(target_time_array[0]) * 60 + int(
                        target_time_array[1]
                    )
                    start_min = start_min + 30
                    diff_hour = start_min / 60
                    if diff_hour.is_integer():
                        target_time = str(math.floor(diff_hour)) + ":00"
                    else:
                        target_time = str(math.floor(diff_hour)) + ":30"
                    # calendar[target_time][booking_date] = False
                    calendar[target_time][booking_date] = schedule.pk
                    if target_time >= end_time:
                        break

        # context['staff'] = staff
        option_times = settings.DAILY_SCHEDULE
        context["calendar"] = calendar
        context["days"] = days
        context["start_day"] = start_day
        context["end_day"] = end_day
        context["before"] = days[0] - datetime.timedelta(days=7)
        context["next"] = days[-1] + datetime.timedelta(days=1)
        context["today"] = today
        context["selected_today"] = selected_today
        context["option_times"] = option_times
        # context['public_holidays'] = settings.PUBLIC_HOLIDAYS
        return context

    def post(self, request, *args, **kwargs):
        if request.POST["start_date"] >= request.POST["end_date"]:
            messages.info(self.request, self.error_message)
            return redirect("student:calendar")
        start_date = request.POST["date"] + " " + request.POST["start_date"] + ":00"
        end_date = request.POST["date"] + " " + request.POST["end_date"] + ":00"
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")

        # calendar = Calendar.objects.filter(id=self.request.POST['id'])
        calendars = Calendar.objects.filter(
            Q(user=self.request.user.id)
            and (Q(start_date__gt=start_date) and Q(end_date__lt=start_date))
            | (Q(start_date__gt=end_date) and Q(end_date__lt=end_date))
        )
        if calendars.exists():
            messages.info(self.request, self.error_message)
            return redirect("student:calendar")

        calendar = Calendar()
        calendar.start_date = start_date
        calendar.end_date = end_date
        calendar.user = User.objects.get(pk=self.request.user.id)
        calendar.content = "入室予約"
        calendar.save()
        return redirect("student:calendar")


class CalendarUpdateView(TemplateView):
    # success_message = "スケジュールは正常に変更されました。"
    error_message = "正しくない時間が入力されていたため、変更されませんでした。"

    def post(self, request, *args, **kwargs):
        if request.POST["start_date"] >= request.POST["end_date"]:
            messages.info(self.request, self.error_message)
            return redirect("student:calendar")
        calendar = Calendar.objects.get(id=self.request.POST["id"])
        start_date = request.POST["date"] + " " + request.POST["start_date"] + ":00"
        end_date = request.POST["date"] + " " + request.POST["end_date"] + ":00"
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
        calendar.start_date = start_date
        calendar.end_date = end_date
        calendar.save()
        return redirect("student:calendar")


class TestView(TemplateView):
    template_name = "student/test.html"

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=self.request.user.id)
        student = Student.objects.get(user=self.request.user.id)
        if student.school is None:
            test_categories = TestCategory.objects.filter(school_category=None)
        else:
            test_categories = TestCategory.objects.filter(
                school_category=student.school.school_category
            )
        test_category = request.GET.get("test_category", None)
        subjects = Subject.objects.filter(
            school_category=student.school.school_category
        )

        return render(
            request,
            self.template_name,
            {"test_categories": test_categories, "subjects": subjects},
        )

    def post(self, request, *args, **kwargs):
        user = User.objects.get(id=self.request.user.id)
        student = Student.objects.get(user=self.request.user.id)
        # test_category = request.POST.get('test_category', None)
        test_category = TestCategory.objects.get(
            id=request.POST.get("test_category", None)
        )
        subjects = request.POST.getlist("subjects", None)
        for subject in subjects:
            test_result = TestResult()
            test_result.test_category = test_category
            test_result.subject = Subject.objects.get(id=subject)
            test_result.school = student.school
            test_result.student = student
            test_result.save()
        return redirect("student:test_result", test_category.pk)


class TestResultView(TemplateView):
    template_name = "student/test_result.html"
    success_message = "テストが保存されました。"

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=self.request.user.id)
        student = Student.objects.get(user=self.request.user.id)
        # self.kwargs['test_category']
        test_results = TestResult.objects.filter(
            student=student, test_category=self.kwargs["test_category"]
        )
        return render(request, self.template_name, {"test_results": test_results})

    def post(self, request, *args, **kwargs):
        user = User.objects.get(id=self.request.user.id)
        student = Student.objects.get(user=self.request.user.id)
        test_result_pks = request.POST.getlist("test_result_pk")
        for test_result_pk in test_result_pks:
            score = request.POST.getlist("score[" + test_result_pk + "]", None)
            score = score[0]
            date = request.POST.getlist("date[" + test_result_pk + "]", None)
            date = date[0]
            test_result = TestResult.objects.get(id=test_result_pk)
            test_result.score = score
            test_result.date = date
            test_result.save()
        messages.info(self.request, self.success_message)
        return redirect("student:test_result", self.kwargs["test_category"])


class AtamaPlusView(CreateView):
    form_class = AtamaPlusForm
    template_name = "student/atamaplus.html"
    success_url = "student:atamaplus"
    model = AtamaPlus

    def dispatch(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)
        # if status_controll.check(self.request.user.id, 99) is False:
        #     return redirect('front:error')
        # else:
        #     return self.get(request, *args, **kwargs)

    def get_initial(self):
        initial = super(AtamaPlusView, self).get_initial()
        try:
            default_value = AtamaPlus.objects.get(user=self.request.user.id)
            initial["login_id"] = default_value.login_id
            initial["password"] = default_value.password
        except AtamaPlus.DoesNotExist:
            initial = None
        return initial


class AtamaPlusUpdateView(TemplateView):
    success_message = "正常に登録されました。"

    def post(self, request, *args, **kwargs):
        try:
            atama_plus = AtamaPlus.objects.get(user=self.request.user.id)
            atama_plus.login_id = self.request.POST["login_id"]
            atama_plus.password = self.request.POST["password"]

            atama_plus.save()
        except AtamaPlus.DoesNotExist or Exception:
            atama_plus = AtamaPlus()
            atama_plus.login_id = self.request.POST["login_id"]
            atama_plus.password = self.request.POST["password"]
            atama_plus.user = User.objects.get(pk=self.request.user.id)
            atama_plus.save()
        messages.info(self.request, self.success_message)
        return redirect("student:atamaplus")


class StudySapuriView(CreateView):
    form_class = AtamaPlusForm
    template_name = "student/studysapuri.html"
    success_url = "student:studysapuri"
    model = StudySapuri

    def dispatch(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)
        # if status_controll.check(self.request.user.id, 99) is False:
        #     return redirect('front:error')
        # else:
        #     return self.get(request, *args, **kwargs)

    def get_initial(self):
        initial = super(StudySapuriView, self).get_initial()
        try:
            default_value = StudySapuri.objects.get(user=self.request.user.id)
            initial["login_id"] = default_value.login_id
            initial["password"] = default_value.password
        except StudySapuri.DoesNotExist:
            initial = None
        return initial


class StudySapuriUpdateView(TemplateView):
    success_message = "正常に登録されました。"

    def post(self, request, *args, **kwargs):
        try:
            atama_plus = StudySapuri.objects.get(user=self.request.user.id)
            atama_plus.login_id = self.request.POST["login_id"]
            atama_plus.password = self.request.POST["password"]

            atama_plus.save()
        except StudySapuri.DoesNotExist or Exception:
            atama_plus = StudySapuri()
            atama_plus.login_id = self.request.POST["login_id"]
            atama_plus.password = self.request.POST["password"]
            atama_plus.user = User.objects.get(pk=self.request.user.id)
            atama_plus.save()
        messages.info(self.request, self.success_message)
        return redirect("student:studysapuri")


class ChatGPTView(TemplateView):
    success_message = "返答が返ってきました。"
    template_name = "student/chatgpt.html"
    openai.api_key = settings.OPENAI_API_KEY

    def get(self, request, *args, **kwargs):
        student = Student.objects.get(user=self.request.user.id)
        # 現在時刻から30分前の時刻を計算
        time_threshold = timezone.now() - datetime.timedelta(hours=1)
        # 30分以内のレコードをフィルタリング
        chat_gpt_logs = ChatGPTLog.objects.filter(
            student=student, created_at__gte=time_threshold
        )

        return render(
            request,
            self.template_name,
            {"chat_gpt_logs": chat_gpt_logs, "student": student},
        )

    def post(self, request, *args, **kwargs):
        request_content = self.request.POST["content"]
        # DeepL APIを使用して翻訳
        translator = deepl.Translator(settings.DEEPL_API_KEY)

        # 日本語->英語
        chatgpt_request = translator.translate_text(
            request_content, source_lang="JA", target_lang="EN-US"
        )

        # ChatGPT APIを使用して応答を生成
        fixed_text = "You are a tutor who specializes in a wide range of subjects. Please respond to the following statement."
        # 応答設定
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # モデルを選択
            messages=[
                {
                    "role": "user",
                    "content": fixed_text + chatgpt_request.text,  # メッセージ
                }
            ],
            max_tokens=1024,  # 生成する文章の最大単語数
            n=1,  # いくつの返答を生成するか
            stop=None,  # 指定した単語が出現した場合、文章生成を打ち切る
            temperature=0.5,  # 出力する単語のランダム性（0から2の範囲） 0であれば毎回返答内容固定
        )

        # 応答
        chatgpt_response = completion.choices[0].message.content
        # 英語->日本語
        response = translator.translate_text(
            chatgpt_response, source_lang="EN", target_lang="JA"
        )
        # 応答内容出力
        # return response

        chatGPT_log = ChatGPTLog()
        chatGPT_log.request_content = request_content
        chatGPT_log.response_content = response.text
        chatGPT_log.student = Student.objects.get(user=self.request.user.id)
        chatGPT_log.save()
        messages.info(self.request, self.success_message)
        return redirect("student:chatgpt")


class MypageView(TemplateView):
    template_name = "student/mypage.html"

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=self.request.user.id)
        student = Student.objects.get(user=self.request.user.id)

        return render(
            request,
            self.template_name,
            {"user_login_id": user.username, "student": student},
        )

    def post(self, request, *args, **kwargs):
        status = request.POST.get("status", None)
        stripe = Stripe()
        student = Student.objects.get(user=self.request.user.id)
        subscription_id = student.stripe_data
        if status == "unsubscribe":
            # 退塾処理
            subscription = stripe.modify_cancel_subscription(subscription_id)
            student.unsubscribe_request = True
            student.save()
            success_message = "退会処理が完了しました。"
        else:
            # 退塾キャンセル処理
            subscription = stripe.modify_not_cancel_subscription(subscription_id)
            student.unsubscribe_request = False
            student.save()
            success_message = "退会キャンセル処理が完了しました。"

        messages.info(self.request, success_message)
        return redirect("student:mypage")


class ProfView(FormView):
    form_class = StudentProfielForm
    template_name = "student/prof.html"
    success_url = "student:prof"

    def dispatch(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get_initial(self):
        initial = super(ProfView, self).get_initial()
        try:
            default_value = Student.objects.get(user=self.request.user.id)
            initial["first_name"] = default_value.first_name
            initial["last_name"] = default_value.last_name
            initial["first_name_kana"] = default_value.first_name_kana
            initial["last_name_kana"] = default_value.last_name_kana
            initial["school"] = default_value.school
            initial["grade"] = default_value.grade
            initial["school_class"] = default_value.school_class
            initial["club_activity"] = default_value.club_activity
            initial["phone_number"] = default_value.phone_number
            initial["parent_first_name"] = default_value.parent_first_name
            initial["parent_last_name"] = default_value.parent_last_name
            initial["parent_first_name_kana"] = default_value.parent_first_name_kana
            initial["parent_last_name_kana"] = default_value.parent_last_name_kana
            initial["parent_phone_number"] = default_value.parent_phone_number
            initial["parent_email"] = default_value.parent_email
            initial["zipcode"] = default_value.zipcode
            initial["prefecture"] = default_value.prefecture
            initial["city"] = default_value.city
            initial["address"] = default_value.address
            initial["introducer_last_name"] = default_value.introducer_last_name
            initial["introducer_first_name"] = default_value.introducer_first_name

        except Student.DoesNotExist:
            user = self.request.user
            initial["first_name"] = user.first_name
            initial["last_name"] = user.last_name
            initial["parent_email"] = user.email
        return initial

    def get_context_data(self, **kwargs):
        context = super(ProfView, self).get_context_data(**kwargs)
        is_paid = (
            Student.objects.filter(user=self.request.user.id)
            .values("stripe_data")
            .first()
        )
        # print(is_paid)
        # print(is_paid['stripe_data'])
        # context['is_paid'] = is_paid['stripe_data']
        # stripe情報がなければTrue
        # context['is_paid'] = True if is_paid['stripe_data'] == None else False
        try:
            if is_paid["stripe_data"]:
                context["is_paid"] = "paid"
            else:
                context["is_paid"] = "not paid"
        except:
            context["is_paid"] = "not account"

        return context


def get_address_from_zipcode(zipcode):
    url = f"http://zipcloud.ibsnet.co.jp/api/search?zipcode={zipcode}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data["results"]:
            prefecture = Prefecture.objects.get(
                prefecture=data["results"][0]["address1"]
            )
            city = City.objects.get(city=data["results"][0]["address2"])
            address = data["results"][0]["address3"]
            data = {"prefecture": prefecture.id, "city": city.id, "address": address}
            return data
        else:
            return None
    else:
        return None


@csrf_exempt
def get_address(request):
    if request.method == "POST":
        zipcode = request.POST.get("zipcode")
        address = get_address_from_zipcode(zipcode)
        return JsonResponse({"address": address})


class ProfUpdateView(TemplateView):
    success_message = "生徒情報が保存されました。"

    def post(self, request, *args, **kwargs):
        try:
            data = Student.objects.get(user=self.request.user.id)
        except (Student.DoesNotExist, Exception):
            data = Student()

        data.first_name = self.request.POST["first_name"]
        data.last_name = self.request.POST["last_name"]
        data.first_name_kana = self.request.POST["first_name_kana"]
        data.last_name_kana = self.request.POST["last_name_kana"]
        data.school = (
            School.objects.get(pk=self.request.POST["school"])
            if self.request.POST["school"]
            else None
        )

        data.grade = self.request.POST["grade"] if self.request.POST["grade"] else None
        data.school_class = (
            self.request.POST["school_class"]
            if self.request.POST["school_class"]
            else None
        )
        data.club_activity = (
            ClubActivity.objects.get(pk=self.request.POST["club_activity"])
            if self.request.POST["club_activity"]
            else None
        )
        data.phone_number = self.request.POST["phone_number"]
        data.parent_first_name = self.request.POST["parent_first_name"]
        data.parent_last_name = self.request.POST["parent_last_name"]
        data.parent_first_name_kana = self.request.POST["parent_first_name_kana"]
        data.parent_last_name_kana = self.request.POST["parent_last_name_kana"]
        data.parent_phone_number = self.request.POST["parent_phone_number"]
        data.parent_email = self.request.POST["parent_email"]
        data.zipcode = self.request.POST["zipcode"]
        data.prefecture = Prefecture.objects.get(pk=self.request.POST["prefecture"])
        data.city = City.objects.get(pk=self.request.POST["city"])
        data.address = self.request.POST["address"]
        data.user = User.objects.get(pk=self.request.user.id)
        data.save()
        is_issued = CouponStudent.objects.filter(student=data).exists()
        if self.request.POST["introducer_first_name"] and is_issued == False:
            introducer_first_name = self.request.POST["introducer_first_name"]
            introducer_last_name = self.request.POST["introducer_last_name"]
            introducer_student = (
                Student.objects.filter(
                    last_name=introducer_last_name, first_name=introducer_first_name
                )
                .exclude(id=data.id)
                .first()
            )
            if introducer_student:
                data.introducer_last_name = introducer_last_name
                data.introducer_first_name = introducer_first_name
                data.save()
                coupon = Coupon.objects.get(id=1)
                # 紹介者のクーポン作成
                coupon_code = generate_coupon_code()

                introducer_coupon = CouponStudent()
                introducer_coupon.coupon = coupon
                introducer_coupon.student = introducer_student
                introducer_coupon.code = coupon_code
                introducer_coupon.save()
                # 入塾者のクーポン作成
                student_coupon = CouponStudent()
                student_coupon.coupon = coupon
                student_coupon.student = data
                introducer_coupon.code = coupon_code
                student_coupon.save()
            else:
                messages.error(self.request, "紹介者の名前が存在しません。")
                return redirect("student:prof")
        else:
            messages.info(self.request, self.success_message)
        if data.stripe_data:
            return redirect("student:mypage")
        else:
            return redirect("student:prof")


import random
import string
import time


# 現在の日時を使用してランダムな文字列を生成する
def generate_coupon_code():
    timestamp = str(int(time.time()))
    rand_str = "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(6)
    )
    coupon_code = timestamp + rand_str
    return coupon_code


# class PaymentView(TemplateView):
#     template_name = 'student/payment/index.html'


class PaymentCheckoutView(TemplateView):
    template_name = "student/payment/checkout.html"


class PaymentSuccessView(TemplateView):
    template_name = "student/payment/success.html"


class PaymentCancelView(TemplateView):
    template_name = "student/payment/cancel.html"


class PaymentView(TemplateView):
    template_name = "student/payment/index.html"

    def post(self, request, *args, **kwargs):
        # ドメイン
        # YOUR_DOMAIN = "http://127.0.0.1:8000"
        # 決済用セッション
        try:
            stripe = Stripe()
            customers = stp.Customer.list(email=request.user.email)
            if customers.data:
                customer_id = customers.data[0].id
            else:
                customer = stp.Customer.create(
                    email=request.user.email, metadata={"user": request.user.id}
                )
                customer_id = customer.id
            # customer = stripe.Customer.create(
            #     email=request.user.email,
            #     metadata={
            #         'user': request.user.id
            #     }
            # )
            checkout_session = stp.checkout.Session.create(
                customer=customer_id,
                # 決済方法
                payment_method_types=["card"],
                # 決済詳細
                line_items=[
                    {
                        "price": "price_1MfbgXKpiWjOWSKI5AbgLgvh",
                        "quantity": 1,
                    }
                ],
                mode="subscription",  # 決済手段（サブスク）
                success_url=f"{request._current_scheme_host}/student/",  # 決済成功時のリダイレクト先
                cancel_url=f"{request._current_scheme_host}/cancel/",  # 決済成功時のリダイレクト先
                metadata={
                    "user": request.user.id,
                },
            )
            return redirect(checkout_session.url)
        except Exception as e:
            # print("Exception: " + str(e))
            return redirect(checkout_session.url)


endpoint_secret = settings.ENDPOINT_SECRET


@csrf_exempt
def handle_stripe_webhook(request):
    payload = request.body
    # sig_header = request.headers.get('stripe-signature')
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        # stripe = Stripe()
        event = stp.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stp.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        from pytz import timezone

        session = event["data"]["object"]
        # Fulfill the purchase...
        # fulfill_order(session)
        student = Student.objects.get(user=session["metadata"]["user"])
        payment_date = datetime.datetime.fromtimestamp(
            session["created"], timezone("Asia/Tokyo")
        )
        expiration_date = payment_date + relativedelta(months=1)
        student.expiration_date = expiration_date
        student.stripe_data = session["subscription"]
        student.entry_date = payment_date
        student.save()

    # Passed signature verification
    return HttpResponse(status=200)


class CouponListView(View):
    def get(self, request):
        student_coupons = CouponStudent.objects.filter(
            student=Student.objects.get(user=request.user.pk), is_used=False
        )
        student_used_coupons = CouponStudent.objects.filter(
            student=Student.objects.get(user=request.user.pk), is_used=True
        )
        return render(
            request,
            "student/coupon_list.html",
            {
                "student_coupons": student_coupons,
                "student_used_coupons": student_used_coupons,
            },
        )


from django.shortcuts import render, get_object_or_404
from django.views import View
import qrcode
from io import BytesIO
from django.http import HttpResponse
from PIL import Image


class QRCodeView(View):
    def get(self, request, code, *args, **kwargs):
        # Get the student_coupon with the given code
        student_coupon = CouponStudent.objects.get(code=code)

        # Generate the QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(code)
        qr.make(fit=True)

        # Create an image from the QR code instance
        img = qr.make_image(fill_color="black", back_color="white")

        # Save the image to a BytesIO object
        response = BytesIO()
        img.save(response, "PNG")
        response.seek(0)

        # Return the image as an HTTP response
        return HttpResponse(response, content_type="image/png")
