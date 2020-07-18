from django.contrib import admin
from django.db.models import Prefetch
from django.utils.html import format_html
from .models import City, Street, Address
from schedule.models import RubbishType
from django.db.models import Case, Value, When, CharField, Count, Q, F, BooleanField
import collections


# Register your models here.
class CityAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    ordering = ("name",)


class StreetAdmin(admin.ModelAdmin):
    search_fields = ("name", "created_date")
    ordering = ("name",)
    list_display = ("name", "created_date")


class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "street",
        "city",
        "all_rubbish_districts_for_address",
        "status_rubbish_districts",
        "status_city_type_in_rubbish_district",
    )
    search_fields = ("city__name", "street__name", "status_for_filter")
    ordering = ("city", "street")
    autocomplete_fields = ("city", "street")
    filter_horizontal = ("rubbish_district",)
    list_filter = (
        "rubbish_district__name",
        "rubbish_district__rubbish_type",
        "rubbish_district__city_type",
        "city",
    )

    fieldsets = [
        ("Adres", {"fields": ["city", "street"]}),
        ("Rejon", {"fields": ["rubbish_district"]}),
    ]

    def all_rubbish_districts_for_address(self, obj):
        rubbish_district_all = (
            obj.rubbish_district.select_related("rubbish_type")
            .only("name", "city_type", "rubbish_type__name")
            .order_by("rubbish_type__name")
        )

        rubbish_types = [district.rubbish_type for district in rubbish_district_all]
        counter_rubbish_types = [
            rubbish_type.name
            for rubbish_type, counter in collections.Counter(rubbish_types).items()
            if counter > 1
        ]

        if counter_rubbish_types:
            return format_html(
                " <br> ".join(
                    f"<b>{district.rubbish_type}</b> - {district.name} ({district.city_type.capitalize()})"
                    if district.rubbish_type.name not in counter_rubbish_types
                    else f"<span style='color: red'><b><u>{district.rubbish_type}</u></b></span> - {district.name} ({district.city_type.capitalize()})"
                    for district in rubbish_district_all
                )
            )
        else:
            return format_html(
                " <br> ".join(
                    f"<b>{district.rubbish_type}</b> - {district.name} ({district.city_type.capitalize()})"
                    if district.city_type == obj.city.city_type
                    else f"<b>{district.rubbish_type}</b> - {district.name} <span style='color: red'><b>(<u>{district.city_type.capitalize()}</u>)</b></span>"
                    for district in rubbish_district_all
                )
            )

    all_rubbish_districts_for_address.short_description = f"Przypisane rejony (docelowo: {RubbishType.objects.count()})"

    def get_queryset(self, request):
        count_rubbish_types = RubbishType.objects.count()

        return (
            super()
            .get_queryset(request)
            .annotate(count_rubbish_districts=Count("rubbish_district"))
            .annotate(
                errors_in_rubbish_districts_city_type=Count(
                    Case(
                        When(
                            ~Q(rubbish_district__city_type=F("city__city_type")),
                            then=F("rubbish_district__city_type"),
                        ),
                        output_field=CharField(),
                    )
                )
            )
            .annotate(distinct_count_rubbish_type=Count("rubbish_district__rubbish_type__name", distinct=True))
            .annotate(
                status_rubbish_districts=Case(
                    When(~Q(count_rubbish_districts=count_rubbish_types) | Q(distinct_count_rubbish_type__lt=F("count_rubbish_districts")), then=False),
                    output_field=BooleanField(),
                    default=True
                )
            )
            .annotate(
                status_city_type_in_rubbish_district=Case(
                    When(~Q(errors_in_rubbish_districts_city_type=0), then=False),
                    output_field=BooleanField(),
                    default=True
                )
            )
            .select_related("city", "street")
            .prefetch_related("rubbish_district")
        )

    def status_rubbish_districts(self, obj):
        return obj.status_rubbish_districts

    status_rubbish_districts.boolean = True
    status_rubbish_districts.short_description = (
        f"Status - rejony"
    )

    def status_city_type_in_rubbish_district(self, obj):
        return obj.status_city_type_in_rubbish_district

    status_city_type_in_rubbish_district.boolean = True
    status_city_type_in_rubbish_district.short_description = "Status - typ miejscowości"


admin.site.register(Street, StreetAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Address, AddressAdmin)
