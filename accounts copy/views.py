from django.contrib import messages
from django.contrib.auth import login, authenticate, REDIRECT_FIELD_NAME
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LogoutView as BaseLogoutView,
    PasswordChangeView as BasePasswordChangeView,
    PasswordResetDoneView as BasePasswordResetDoneView,
    PasswordResetConfirmView as BasePasswordResetConfirmView,
)
from django.shortcuts import get_object_or_404, redirect
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.utils.http import url_has_allowed_host_and_scheme as is_safe_url
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters


from django.views.generic import View, FormView, CreateView
from django.conf import settings
from .forms import SignUpForm, SignInViaUsernameForm
from .models import UserStatus
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .forms import CustomPasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import ObjectDoesNotExist


class GuestOnlyView(View):
    def dispatch(self, request, *args, **kwargs):
        # Redirect to the index page if the user already authenticated
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)

        return super().dispatch(request, *args, **kwargs)


class SignUpView(GuestOnlyView, FormView):
    template_name = "accounts/sign_up.html"
    form_class = SignUpForm

    def form_valid(self, form):
        request = self.request
        user = form.save(commit=False)
        user.is_active = True
        user.save()

        user_status = UserStatus()
        user_status.status = 0  # Student
        user_status.user = user
        user_status.save()

        raw_password = form.cleaned_data["password1"]

        user = authenticate(username=user.username, password=raw_password)
        login(request, user)

        messages.success(request, _("You are successfully signed up!"))

        return redirect("student:prof")

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class LogInView(GuestOnlyView, FormView):
    template_name = "accounts/log_in.html"

    @staticmethod
    def get_form_class(**kwargs):
        # if settings.DISABLE_USERNAME or settings.LOGIN_VIA_EMAIL:
        #     return SignInViaEmailForm

        # if settings.LOGIN_VIA_EMAIL_OR_USERNAME:
        #     return SignInViaEmailOrUsernameForm

        return SignInViaUsernameForm

    @method_decorator(sensitive_post_parameters("password"))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        request = self.request

        # If the test cookie worked, go ahead and delete it since its no longer needed
        # if request.session.test_cookie_worked():
        #     request.session.delete_test_cookie()

        # The default Django's "remember me" lifetime is 2 weeks and can be changed by modifying
        # the SESSION_COOKIE_AGE settings' option.
        # if settings.USE_REMEMBER_ME:
        #     if not form.cleaned_data['remember_me']:
        #         request.session.set_expiry(0)

        login(request, form.user_cache)

        try:
            user_status = UserStatus.objects.get(user=self.request.user.id)
            if user_status.status == 0:
                return redirect("student:index")
            if user_status.status == 1:
                return redirect("trainer:index")
        except ObjectDoesNotExist:
            logout(request, form.user_cache)
            return redirect(settings.LOGIN_REDIRECT_URL)
        # if user_status.status == 2:
        #     return redirect('trainer:index')


class LogOutView(LoginRequiredMixin, BaseLogoutView):
    template_name = "accounts/log_in.html"
    # template_name = 'accounts/log_out.html'
    # return redirect('accounts:log_in')


class PasswordChangeView(LoginRequiredMixin, FormView):
    form_class = CustomPasswordChangeForm
    template_name = "accounts/password_change.html"
    success_url = reverse_lazy("student:mypage")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        # パスワードが変更された後もユーザーがログイン状態を維持できるようにする
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)
