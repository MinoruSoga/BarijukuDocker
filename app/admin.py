from django.contrib import admin

from .models import Prefecture,Place


class PrefectureAdmin(admin.ModelAdmin):
    pass
class PlaceAdmin(admin.ModelAdmin):
    pass

admin.site.register(Prefecture, PrefectureAdmin)
admin.site.register(Place, PlaceAdmin)
