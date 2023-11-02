from django.contrib import admin

from .models import UserStatus
from .forms import UserStatusAdminForm


class UserStatusAdmin(admin.ModelAdmin):
  form = UserStatusAdminForm

admin.site.register(UserStatus, UserStatusAdmin)
