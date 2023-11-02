from django.urls import path
from . import views

app_name = 'student'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('calendar/<int:year>/<int:month>/<int:day>/', views.CalendarView.as_view(), name='calendar'),
    path('calendar_update/', views.CalendarUpdateView.as_view(), name='calendar_update'),

    # テスト登録
    path('test/', views.TestView.as_view(), name='test'),
    path('test_result/<int:test_category>', views.TestResultView.as_view(), name='test_result'),

    # Atama+
    path('atamaplus/', views.AtamaPlusView.as_view(), name='atamaplus'),
    path('atamaplus_update/', views.AtamaPlusUpdateView.as_view(), name='atamaplus_update'),
    # Study Sapuri
    path('studysapuri/', views.StudySapuriView.as_view(), name='studysapuri'),
    path('studysapuri_update/', views.StudySapuriUpdateView.as_view(), name='studysapuri_update'),

    # ChatGPT
    path('chatgpt/', views.ChatGPTView.as_view(), name='chatgpt'),

    # マイページ
    path('mypage/', views.MypageView.as_view(), name='mypage'),

    # 生徒情報
    path('prof/', views.ProfView.as_view(), name='prof'),
    path('get_address/', views.get_address, name='get_address'),
    path('prof_update/', views.ProfUpdateView.as_view(), name='prof_update'),

    path('payment/', views.PaymentView.as_view(), name='payment'),
    path('checkout/', views.PaymentCheckoutView.as_view(), name='checkout'),
    # path('create_checkout_session/', views.create_checkout_session, name='checkout_session'),
    path('success/', views.PaymentSuccessView.as_view(), name='success'),
    path('cancel/', views.PaymentCancelView.as_view(), name='cancel'),
    path("stripe/webhook/", views.handle_stripe_webhook, name="stripe_webhook"),

    # path('staff/<int:pk>/calendar/<int:year>/<int:month>/<int:day>/', views.StaffCalendar.as_view(), name='calendar'),
    # path('issue_coupon/', views.IssueCouponView.as_view(), name='issue_coupon'),
    path('coupon-list/', views.CouponListView.as_view(), name='coupon_list'),
    path('qrcode/<str:code>/', views.QRCodeView.as_view(), name='qrcode'),


]
