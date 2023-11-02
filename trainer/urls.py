from django.urls import path
from . import views

app_name = 'trainer'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('meeting/', views.MeetingView.as_view(), name='meeting'),
    path('calendar_select/', views.CalendarSelectView.as_view(), name='calendar_select'),
    path('calendar/<int:pk>', views.CalendarView.as_view(), name='calendar'),
    path('calendar/<int:pk>/<int:year>/<int:month>/<int:day>/', views.CalendarView.as_view(), name='calendar'),
    # path('calendar/', views.CalendarView.as_view(), name='calendar'),

    # マイページ
    path('mypage/', views.MypageView.as_view(), name='mypage'),
    # トレーナー情報
    path('prof/', views.ProfView.as_view(), name='prof'),
    path('get_address/', views.get_address, name='get_address'),
    path('prof_update/', views.ProfUpdateView.as_view(), name='prof_update'),
    path('meeting/<int:pk>', views.MeetingView.as_view(), name='meeting'),
]
