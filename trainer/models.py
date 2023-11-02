from django.db import models

# from django.contrib.auth.models import User
from app.models import Prefecture, City

from django.conf import settings

User = settings.AUTH_USER_MODEL


class Trainer(models.Model):
    last_name = models.CharField("性", max_length=50)
    first_name = models.CharField("名", max_length=50)
    last_name_kana = models.CharField("性 カナ", max_length=50)
    first_name_kana = models.CharField("名 カナ", max_length=50)
    phone_number = models.DecimalField(max_digits=12, decimal_places=0, null=True)
    email = models.CharField("メールアドレス", max_length=50, null=True)
    zipcode = models.CharField("郵便番号", max_length=50, null=True)
    prefecture = models.ForeignKey(Prefecture, on_delete=models.CASCADE, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)
    address = models.CharField("番地以降", max_length=50, null=True)
    entry_date = models.DateField("入社日", null=True)
    # user_id = models.ForeignKey(User, verbose_name='AuthUser', on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.last_name
