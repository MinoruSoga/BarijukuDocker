from django.urls import path
from . import views

# from .views import save_qr_code


app_name = "shop"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("prof/", views.ProfView.as_view(), name="prof"),
    path("prof_update/", views.ProfUpdateView.as_view(), name="prof_update"),
    path("redeem_coupon/", views.RedeemCouponView.as_view(), name="redeem_coupon"),
]
