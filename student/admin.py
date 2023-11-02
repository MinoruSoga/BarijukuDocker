from django.contrib import admin

# Register your models here.
from .models import School, SchoolCategory, ClubActivity, TestCategory, Subject


class SchoolAdmin(admin.ModelAdmin):
    pass
class SchoolCategoryAdmin(admin.ModelAdmin):
    pass
class ClubActivityAdmin(admin.ModelAdmin):
    pass
class TestCategoryAdmin(admin.ModelAdmin):
    pass
class SubjectAdmin(admin.ModelAdmin):
    pass

admin.site.register(School, SchoolAdmin)
admin.site.register(SchoolCategory, SchoolCategoryAdmin)
admin.site.register(ClubActivity, ClubActivityAdmin)
admin.site.register(TestCategory, TestCategoryAdmin)
admin.site.register(Subject, SubjectAdmin)
