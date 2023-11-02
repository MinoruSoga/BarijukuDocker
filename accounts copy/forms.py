
from datetime import timedelta

from django import forms
from django.forms import ValidationError
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from .models import UserStatus
from django.contrib.auth.forms import PasswordChangeForm

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = settings.SIGN_UP_FIELDS

    email = forms.EmailField(label=_('Email'), help_text=_('Required. Enter an existing email address.'))

    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username=username).exists():
            raise ValidationError('入力されたログインIDは使用できません。')

        return username

    def clean_email(self):
        email = self.cleaned_data['email']

        user = User.objects.filter(email__iexact=email).exists()
        if user:
            raise ValidationError('入力されたメールアドレスは使用できません。')

        return email
class UserCacheMixin:
    user_cache = None

class SignIn(UserCacheMixin, forms.Form):
    password = forms.CharField(label=_('Password'), strip=False, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if settings.USE_REMEMBER_ME:
            self.fields['remember_me'] = forms.BooleanField(label=_('Remember me'), required=False)

    def clean_password(self):
        password = self.cleaned_data['password']

        if not self.user_cache:
            return password

        if not self.user_cache.check_password(password):
            raise ValidationError(_('You entered an invalid password.'))

        return password

class SignInViaUsernameForm(SignIn):
    username = forms.CharField(label=_('Username'))

    @property
    def field_order(self):
        if settings.USE_REMEMBER_ME:
            return ['username', 'password', 'remember_me']
        return ['username', 'password']

    def clean_username(self):
        username = self.cleaned_data['username']

        user = User.objects.filter(username=username).first()
        if not user:
            raise ValidationError(_('You entered an invalid username.'))

        if not user.is_active:
            raise ValidationError(_('This account is not active.'))

        self.user_cache = user

        return username

class UserStatusAdminForm(forms.ModelForm):
    class Meta:
        model = UserStatus
        STATUS_CHOICE = [
            ('0', '生徒'),
            ('1', 'スタディトレーナー'),
            ('2', '管理者'),
            ('3', '提携店舗'),
        ]

        fields = ['user', 'status']
        # status     = forms.Select(  widget  = forms.Select( attrs={ "maxlength":str(UserStatus.comment.field.max_length), } ),label   = UserStatus.comment.field.verbose_name )
        widgets = {
            'status': forms.Select(choices=STATUS_CHOICE),
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    pass  # 任意のカスタマイズが必要な場合はここで追加
