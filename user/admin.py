from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    # カスタムユーザーモデルのフィールドに基づいてfieldsetsを更新
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'user_type')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    # add_fieldsetsはユーザーを追加するためのフォームで使用されます
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'user_type'),
        }),
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_staff')
    list_filter = ('user_type', 'is_staff', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)
