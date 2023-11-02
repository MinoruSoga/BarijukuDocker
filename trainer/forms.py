from django import forms
from .models import Trainer
from django.utils.translation import gettext_lazy as _


class TrainerProfielForm(forms.ModelForm):

    class Meta:
        model = Trainer
        fields = (
        'first_name',
        'last_name',
        'first_name_kana',
        'last_name_kana',
        'phone_number',
        'email',
        'zipcode',
        'prefecture',
        'city',
        'address',
        )
