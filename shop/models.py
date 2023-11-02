from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL

class Shop(models.Model):
    shop_name = models.CharField(max_length=100)
    email = models.CharField('メールアドレス', max_length=50, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bank_name = models.CharField('銀行名', max_length=100)
    branch_name = models.CharField('支店名', max_length=100)
    account_number = models.CharField('口座番号', max_length=20)
    account_holder_name = models.CharField('口座名義人', max_length=100)
    def __str__(self):
        return self.shop_name

