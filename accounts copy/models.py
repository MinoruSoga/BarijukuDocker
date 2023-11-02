from django.db import models
from django.contrib.auth.models import User


class UserStatus(models.Model):
    # user_id = models.ForeignKey(User, verbose_name='auth_user_id', on_delete=models.SET_NULL, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.IntegerField('ステータス')

# 0 student
# 1 trainer
# 2 admin
# 3 shop
