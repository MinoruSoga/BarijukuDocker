from django import forms
from .models import AtamaPlus, Student
from django.utils.translation import gettext_lazy as _
from app.models import Coupon, Prefecture, City


class AtamaPlusForm(forms.ModelForm):
    class Meta:
        model = AtamaPlus
        fields = ("login_id", "password")


class StudySapuriForm(forms.ModelForm):
    class Meta:
        model = AtamaPlus
        fields = ("login_id", "password")


class StudentProfielForm(forms.ModelForm):
    class Meta:
        model = Student
        GRADE_CHOICES = [
            ("", "---"),
            ("1", "1年"),
            ("2", "2年"),
            ("3", "3年"),
            ("4", "4年"),
            ("5", "5年"),
            ("6", "6年"),
        ]
        CLASS_CHOICES = [
            ("", "---"),
            ("1", "1組"),
            ("2", "2組"),
            ("3", "3組"),
            ("4", "4組"),
            ("5", "5組"),
            ("6", "6組"),
            ("7", "7組"),
        ]
        fields = (
            "first_name",
            "last_name",
            "first_name_kana",
            "last_name_kana",
            "school",
            "grade",
            "school_class",
            "club_activity",
            "phone_number",
            "parent_first_name",
            "parent_last_name",
            "parent_first_name_kana",
            "parent_last_name_kana",
            "parent_phone_number",
            "parent_email",
            "zipcode",
            "prefecture",
            "city",
            "address",
            "introducer_last_name",
            "introducer_first_name",
        )

        widgets = {
            "grade": forms.Select(
                choices=GRADE_CHOICES, attrs={"class": "form-control"}
            ),
            "school_class": forms.Select(
                choices=CLASS_CHOICES, attrs={"class": "form-control"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # activeがTrueのPrefectureオブジェクトを取得してchoicesに設定
        active_prefectures = Prefecture.objects.filter(is_active=True)
        self.fields["prefecture"].queryset = active_prefectures

        active_cities = City.objects.filter(is_active=True)
        self.fields["city"].queryset = active_cities
