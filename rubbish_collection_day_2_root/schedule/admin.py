from django.contrib import admin
from .models import Date, RubbishType, RubbishDistrict, ScheduleConfiguration
from solo.admin import SingletonModelAdmin


# Register your models here.
class DateAdmin(admin.ModelAdmin):
    search_fields = ("date",)
    ordering = ("date",)


class RubbishDistrictAdmin(admin.ModelAdmin):
    list_display = ("name", "rubbish_type", "city_type")
    search_fields = ("name", "city_type", "rubbish_type")
    list_filter = ("city_type", "rubbish_type", "name")
    ordering = ("city_type", "rubbish_type", "name")
    filter_horizontal = ("date",)
    autocomplete_fields = ("rubbish_type",)

    fieldsets = [
        ("Rejon", {"fields": ["rubbish_type", "name", "city_type"]}),
        ("Terminy odbioru odpadów", {"fields": ["date"]}),
    ]


class RubbishDistrictInline(admin.TabularInline):
    model = RubbishDistrict
    fields = ("name", "city_type")
    ordering = ("city_type", "name")


class RubbishTypeAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    ordering = ("name",)

    inlines = [
        RubbishDistrictInline,
    ]


admin.site.register(Date, DateAdmin)
admin.site.register(RubbishType, RubbishTypeAdmin)
admin.site.register(RubbishDistrict, RubbishDistrictAdmin)
admin.site.register(ScheduleConfiguration, SingletonModelAdmin)
