from django.urls import path

# from . import views
from .views import CustomLoginView, RegisterView, logout_view

app_name = "user"
urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    # path('register/', views.register, name='register'),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", logout_view, name="logout"),
    # path('student/', views.StudentView.as_view(), name='student_view'),
    # path('trainer/', views.TrainerView.as_view(), name='trainer_view'),
    # path('shop/', views.ShopView.as_view(), name='shop_view'),
]
