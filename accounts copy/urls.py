from django.urls import path

# from .views import (
#     LogInView, ResendActivationCodeView, RemindUsernameView, SignUpView, ActivateView, LogOutView,
#     ChangeEmailView, ChangeEmailActivateView, ChangeProfileView, ChangePasswordView,
#     RestorePasswordView, RestorePasswordDoneView, RestorePasswordConfirmView,
# )
from .views import (
    SignUpView, LogInView, LogOutView, PasswordChangeView
)

app_name = 'accounts'

urlpatterns = [
    # ex: /accounts/signup/
    path('sign-up/', SignUpView.as_view(), name='sign_up'),
    path('log-in/', LogInView.as_view(), name='log_in'),
    path('log-out/', LogOutView.as_view(), name='log_out'),
    # path('login/', views.LoginViewCustom.as_view(), name='login'),
    path('password_change/', PasswordChangeView.as_view(), name='password_change'),
]
