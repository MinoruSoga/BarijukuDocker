from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth import get_user_model
from django.forms import ValidationError
User = get_user_model()

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2')
    # def clean_username(self):
    #     username = self.cleaned_data['username']

    #     if User.objects.filter(username=username).exists():
    #         raise ValidationError('入力されたログインIDは使用できません。')

    #     return username
