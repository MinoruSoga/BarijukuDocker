from django.shortcuts import render, redirect
from django.views.generic import (
    DetailView,
    FormView,
    ListView,
    TemplateView,
    View,
    CreateView,
)
from .forms import ShopProfielForm
from .models import Shop
from django.contrib import messages
from django.contrib.auth import get_user_model
from app.models import CouponStudent
from django.utils import timezone

User = get_user_model()


class IndexView(TemplateView):
    template_name = "shop/index.html"

    def get(self, request, *args, **kwargs):
        template_name = "shop/index.html"
        student_coupons = CouponStudent.objects.filter(
            shop=Shop.objects.get(user=request.user), is_used=True
        )
        return render(request, self.template_name, {"student_coupons": student_coupons})


class ProfView(FormView):
    form_class = ShopProfielForm
    template_name = "shop/prof.html"
    success_url = "shop:prof"

    def dispatch(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get_initial(self):
        initial = super(ProfView, self).get_initial()
        try:
            self.request.user.id = 4
            default_value = Shop.objects.get(user=self.request.user.id)
            initial["shop_name"] = default_value.shop_name
            initial["email"] = default_value.email
            initial["bank_name"] = default_value.bank_name
            initial["branch_name"] = default_value.branch_name
            initial["account_number"] = default_value.account_number
            initial["account_holder_name"] = default_value.account_holder_name

        except Shop.DoesNotExist:
            user = self.request.user
        return initial


class ProfUpdateView(TemplateView):
    success_message = "店舗情報が登録されました。"

    def post(self, request, *args, **kwargs):
        try:
            self.request.user.id = 4
            data = Shop.objects.get(user=self.request.user.id)
        except (Shop.DoesNotExist, Exception):
            data = Shop()

        data.shop_name = self.request.POST["shop_name"]
        data.email = self.request.POST["email"]
        data.bank_name = self.request.POST["bank_name"]
        data.branch_name = self.request.POST["branch_name"]
        data.account_number = self.request.POST["account_number"]
        data.account_holder_name = self.request.POST["account_holder_name"]

        # self.request.user.id = data.user
        data.user = User.objects.get(pk=self.request.user.id)
        data.save()
        messages.info(self.request, self.success_message)
        return redirect("shop:prof")


class RedeemCouponView(TemplateView):
    template_name = "shop/redeem_coupon.html"

    def get(self, request, *args, **kwargs):
        code = request.GET.get("code", None)
        if code:
            coupon_student = CouponStudent.objects.filter(
                code=code, is_used=False
            ).first()
            if coupon_student:
                coupon_student.is_used = True
                coupon_student.shop = Shop.objects.get(user=request.user)
                coupon_student.used_date = timezone.now()
                coupon_student.save()
                messages.success(request, "クーポンが正常に引き換えられました。")
            else:
                messages.error(request, "無効なクーポンコードです。")
        return render(request, self.template_name)
