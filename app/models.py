from django.db import models

# from django.contrib.auth.models import User
# from student.models import Student
# from trainer.models import Trainer
from django.contrib.auth.models import AbstractUser

from django.conf import settings

User = settings.AUTH_USER_MODEL


class Prefecture(models.Model):
    prefecture = models.CharField("都道府県", max_length=50)
    is_active = models.BooleanField(verbose_name="有効かどうか", default=False)

    def __str__(self):
        return self.prefecture


class City(models.Model):
    city = models.CharField("市町村", max_length=50)
    prefecture = models.ForeignKey(Prefecture, on_delete=models.CASCADE)
    is_active = models.BooleanField(verbose_name="有効かどうか", default=False)

    def __str__(self):
        return self.city


class Place(models.Model):
    place_name = models.CharField("名称", max_length=50, null=True)
    postal_code = models.CharField("郵便番号", max_length=50, null=True)
    prefecture = models.ForeignKey(Prefecture, on_delete=models.CASCADE, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)
    address = models.CharField("番地以降", max_length=50, null=True)
    entry_date = models.DateField("開校日", null=True)


class Calendar(models.Model):
    start_date = models.DateTimeField("開始日時")
    end_date = models.DateTimeField("終了日時")
    user = models.ForeignKey(User, verbose_name="AuthUser", on_delete=models.CASCADE)
    is_student = models.IntegerField(default=1)
    content = models.CharField("内容", max_length=50, null=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.start_date)


class MeetingSchedule(models.Model):
    start_date = models.DateTimeField("開始日時")
    end_date = models.DateTimeField("終了日時")
    student = models.ForeignKey("student.Student", on_delete=models.CASCADE)
    trainer = models.ForeignKey("trainer.Trainer", on_delete=models.CASCADE)
    content = models.CharField("内容", max_length=50, null=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class Meeting(models.Model):
    meeting_schedule = models.ForeignKey(MeetingSchedule, on_delete=models.CASCADE)
    content = models.CharField("内容", max_length=50, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content


class ChatGPTLog(models.Model):
    request_content = models.TextField("リクエスト内容", null=True)
    response_content = models.TextField("レスポンス内容", null=True)
    student = models.ForeignKey("student.Student", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.request_content


from django.utils.crypto import get_random_string


class Coupon(models.Model):
    title = models.CharField("クーポン名", max_length=50, null=True)
    type = models.CharField("クーポンタイプ", max_length=50, null=True)
    price = models.IntegerField(default=1000)
    is_active = models.BooleanField(verbose_name="有効かどうか", default=True)

    def __str__(self):
        return self.title


# 生徒が所持しているクーポン
class CouponStudent(models.Model):
    code = models.CharField(
        "クーポンコード", max_length=20, unique=True, default=get_random_string(length=10)
    )
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    student = models.ForeignKey("student.Student", on_delete=models.CASCADE)
    is_used = models.BooleanField(verbose_name="使用済", default=False)
    expiration_date = models.DateField("有効期限", null=True, blank=True)
    shop = models.ForeignKey(
        "shop.Shop", on_delete=models.CASCADE, null=True, blank=True
    )
    used_date = models.DateTimeField("利用日時", null=True, blank=True)

    def __str__(self):
        return self.code
