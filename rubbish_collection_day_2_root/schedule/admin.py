from django.contrib import admin, messages
from django.db import IntegrityError

from django.urls import path
from django.http import HttpResponseRedirect
from .models import Date, RubbishType, RubbishDistrict, ScheduleConfiguration
from solo.admin import SingletonModelAdmin
from datetime import datetime, timedelta


# Register your models here.
class DateAdmin(admin.ModelAdmin):
    search_fields = ("date",)
    ordering = ("date",)
    change_list_template = "admin/schedule/date/date_change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [path("add-many-dates/", self.add_many_dates)]
        return custom_urls + urls

    def add_many_dates(self, request):
        if request.method == "POST":
            start_date = datetime.strptime(
                request.POST.get("start-date"), "%Y-%m-%d"
            ).date()
            end_date = datetime.strptime(
                request.POST.get("end-date"), "%Y-%m-%d"
            ).date()

            delta = end_date - start_date
            add_new_dates = None
            for i in range(delta.days + 1):
                day = start_date + timedelta(days=i)

                try:
                    Date.objects.create(date=day)
                except IntegrityError:
                    self.message_user(
                        request, f"Ta data już istnieje: {day}",
                        level=messages.ERROR
                    )
                else:
                    add_new_dates = True
            if add_new_dates:
                self.message_user(request, "Dodano nowe daty")
        return HttpResponseRedirect("../")


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
