from django.contrib import admin
from .models import Date, RubbishType, RubbishDistrict, ScheduleConfiguration
from solo.admin import SingletonModelAdmin


# Register your models here.
class DateAdmin(admin.ModelAdmin):
    search_fields = ("date",)
    ordering = ("date",)


class RubbishTypeAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    ordering = ("name",)


class RubbishDistrictAdmin(admin.ModelAdmin):
    search_fields = ("name", "city_type", "rubbish_type")
    ordering = ("city_type", "name")


admin.site.register(Date, DateAdmin)
admin.site.register(RubbishType, RubbishTypeAdmin)
admin.site.register(RubbishDistrict, RubbishDistrictAdmin)
admin.site.register(ScheduleConfiguration, SingletonModelAdmin)