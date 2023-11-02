from django.shortcuts import render, redirect
from django.views.generic import (
    DetailView,
    FormView,
    ListView,
    TemplateView,
    View,
    CreateView
)
from student.models import AtamaPlus, StudySapuri, Student
from trainer.models import Trainer
from app.models import Calendar, Prefecture, City, MeetingSchedule, Place, Meeting 
from django.db.models import Q
import datetime
from django.conf import settings
from django.utils import timezone
import math
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .forms import TrainerProfielForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.contrib import messages

class IndexView(TemplateView):
    template_name = 'trainer/index.html'
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
            meeting_schedules = MeetingSchedule.objects.filter(trainer=Trainer.objects.get(user=self.request.user.id))
        except:
            meeting_schedules = None
        return render(request, self.template_name, {'atama_plus': atama_plus, 'study_sapuri': study_sapuri, 'meeting_schedules': meeting_schedules })
class MeetingView(TemplateView):
    template_name = 'trainer/meeting.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['meeting'] = Meeting.objects.get(meeting_schedule_id=self.kwargs['pk'])
        except Meeting.DoesNotExist:
            context['meeting'] = None
        return context
    
    def post(self, request, *args, **kwargs):
        try:
            meeting = Meeting.objects.get(meeting_schedule_id=self.kwargs['pk'])
        except Meeting.DoesNotExist:
            meeting = Meeting()
        meeting.content = request.POST['content']
        meeting.meeting_schedule_id = self.kwargs['pk']
        meeting.save()
        if request.POST['type'] == 'save':
            messages.info(self.request, "保存されました。")
            return redirect('trainer:index')
        else:
            messages.info(self.request, "一時保存されました。")
            return redirect('trainer:meeting', self.kwargs['pk'])

class CalendarSelectView(TemplateView):
    template_name = 'trainer/student.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        students = Student.objects.all()
        # students = Student.objects.filter(user__is_active=True)

        context['students'] = students
        return context
    def post(self, request, *args, **kwargs):
        print(request.POST['student'])
        return redirect('trainer:calendar', request.POST['student'])
class CalendarView(TemplateView):
    template_name = 'trainer/calendar.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = get_object_or_404(Student, pk=self.kwargs['pk'])
        today = datetime.date.today()
        selected_today = datetime.date.today().strftime("%Y-%m-%d")

        # どの日を基準にカレンダーを表示するかの処理。
        # 年月日の指定があればそれを、なければ今日からの表示。
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
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
        start_time = datetime.datetime.combine(start_day, datetime.time(hour=10, minute=0, second=0))
        end_time = datetime.datetime.combine(end_day, datetime.time(hour=23, minute=0, second=0))
        

        # for schedule in Calendar.objects.filter(user=self.request.user.id).exclude(Q(start_date__gt=end_time) | Q(end_date__lt=start_time)):
        for schedule in Calendar.objects.filter(user=student.user.id).exclude(Q(start_date__gt=end_time) | Q(end_date__lt=start_time)):
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
                    target_time_array = target_time.split(':')
                    start_min = int(target_time_array[0]) * 60 + int(target_time_array[1])
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


        context['student'] = student
        option_times = settings.DAILY_SCHEDULE
        context['calendar'] = calendar
        context['days'] = days
        context['start_day'] = start_day
        context['end_day'] = end_day
        context['before'] = days[0] - datetime.timedelta(days=7)
        context['next'] = days[-1] + datetime.timedelta(days=1)
        context['today'] = today
        context['selected_today'] = selected_today
        context['option_times'] = option_times
        # context['public_holidays'] = settings.PUBLIC_HOLIDAYS
        return context
    def post(self, request, *args, **kwargs):
        start_date = request.POST['date'] + " " +request.POST['start_date'] + ":00"
        # end_date = request.POST['date'] + " " +request.POST['end_date'] + ":00"
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
        # end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
        end_date = start_date + datetime.timedelta(minutes=30)
        meeting_schedule = MeetingSchedule()
        meeting_schedule.start_date = start_date
        meeting_schedule.end_date = end_date
        student = get_object_or_404(Student, pk=self.kwargs['pk'])
        trainer = get_object_or_404(Trainer, user=self.request.user.id)
        meeting_schedule.student = student
        meeting_schedule.trainer = trainer
        meeting_schedule.content = "面談"
        meeting_schedule.place = Place.objects.get(id=1)
        meeting_schedule.save()
        return redirect('trainer:index')

    
class MypageView(TemplateView):
    template_name = 'trainer/mypage.html'
    
    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=self.request.user.id)
        try:
            trainer = Trainer.objects.get(user=self.request.user.id)
        except Trainer.DoesNotExist:
            trainer = None
        
        return render(request, self.template_name, {'user_login_id': user.username, 'trainer': trainer})
    # def post(self, request, *args, **kwargs):
    #     status = request.POST.get('status', None)
    #     stripe = Stripe()
    #     student = Student.objects.get(user=self.request.user.id)
    #     subscription_id = student.stripe_data
    #     if status == 'unsubscribe':
    #         # 退塾処理
    #         subscription = stripe.modify_cancel_subscription(subscription_id)
    #         student.unsubscribe_request = True
    #         student.save()
    #         success_message = "退会処理が完了しました。"
    #     else:
    #         # 退塾キャンセル処理
    #         subscription = stripe.modify_not_cancel_subscription(subscription_id)
    #         student.unsubscribe_request = False
    #         student.save()
    #         success_message = "退会キャンセル処理が完了しました。"

    #     messages.info(self.request, success_message)
    #     return redirect('student:mypage')

class ProfView(FormView):
    form_class = TrainerProfielForm
    template_name = 'trainer/prof.html'
    success_url = 'trainer:prof'

    def dispatch(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)
    
    def get_initial(self):
        initial = super(ProfView, self).get_initial()
        try:
            default_value = Trainer.objects.get(user=self.request.user.id)
            initial['first_name'] = default_value.first_name
            initial['last_name'] = default_value.last_name
            initial['first_name_kana'] = default_value.first_name_kana
            initial['last_name_kana'] = default_value.last_name_kana
            initial['email'] = default_value.email
            initial['zipcode'] = default_value.zipcode
            initial['prefecture'] = default_value.prefecture
            initial['city'] = default_value.city
            initial['address'] = default_value.address

        except Trainer.DoesNotExist:
            user = self.request.user
            initial['first_name'] = user.first_name
            initial['last_name'] = user.last_name
            initial['email'] = user.email
        return initial
    # def get_context_data(self, **kwargs):
    #     context = super(ProfView, self).get_context_data(**kwargs)
    #     is_paid = Student.objects.filter(user=self.request.user.id).values('stripe_data').first()
    #     # print(is_paid)
    #     # print(is_paid['stripe_data'])
    #     # context['is_paid'] = is_paid['stripe_data']
    #     # stripe情報がなければTrue 
    #     # context['is_paid'] = True if is_paid['stripe_data'] == None else False
    #     try:
    #         if is_paid['stripe_data']:
    #             context['is_paid'] = 'paid'
    #         else:
    #             context['is_paid'] = 'not paid'
    #     except:
    #         context['is_paid'] = 'not account'


    #     return context
def get_address_from_zipcode(zipcode):
    url = f"http://zipcloud.ibsnet.co.jp/api/search?zipcode={zipcode}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data["results"]:
            prefecture = Prefecture.objects.get(prefecture=data["results"][0]["address1"])
            city = City.objects.get(city=data["results"][0]["address2"])
            address = data["results"][0]["address3"]
            data = {
                "prefecture": prefecture.id,
                "city": city.id,
                "address": address
            }
            return data
        else:
            return None
    else:
        return None
@csrf_exempt
def get_address(request):
    if request.method == 'POST':
        zipcode = request.POST.get('zipcode')
        address = get_address_from_zipcode(zipcode)
        return JsonResponse({'address': address})

class ProfUpdateView(TemplateView):
    success_message = "生徒情報が登録されました。"
    def post(self,request, *args, **kwargs):
        try:
            data = Trainer.objects.get(user=self.request.user.id)
        except (Trainer.DoesNotExist, Exception):
            data = Trainer()
        data.first_name = self.request.POST['first_name']
        data.last_name = self.request.POST['last_name']
        data.first_name_kana = self.request.POST['first_name_kana']
        data.last_name_kana = self.request.POST['last_name_kana']
        
        data.phone_number = self.request.POST['phone_number']
        data.email = self.request.POST['email']
        data.zipcode = self.request.POST['zipcode']
        data.prefecture = Prefecture.objects.get(pk=self.request.POST['prefecture'])
        data.city = City.objects.get(pk=self.request.POST['city'])
        data.address = self.request.POST['address']

        data.user = User.objects.get(pk=self.request.user.id)
        data.save()
        messages.info(self.request, self.success_message)
        return redirect('trainer:mypage')
