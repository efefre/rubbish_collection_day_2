from django.contrib import admin
from django.db.models import Prefetch
from django.utils.html import format_html
from django.db.utils import ProgrammingError
from .models import City, Street, Address
from schedule.models import RubbishType, RubbishDistrict
from django.db.models import Case, Value, When, CharField, Count, Q, F, BooleanField
import collections


# Register your models here.
class CityAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    ordering = ("name",)

class AddressInline(admin.TabularInline):
    model = Address
    fields = ("city",)
    ordering = ("city", )

class StreetAdmin(admin.ModelAdmin):
    search_fields = ("name", "created_date")
    ordering = ("name",)
    list_display = ("name", "created_date", "count_addresses_with_this_street")

    inlines = [
        AddressInline,
    ]

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(count_addresses_with_this_street=Count("address")))

    def count_addresses_with_this_street(self, obj):
        return obj.count_addresses_with_this_street

    count_addresses_with_this_street.short_description = "Liczba adresów z ulicą"
    count_addresses_with_this_street.admin_order_field = "count_addresses_with_this_street"


def add_big_rubbish_district_1(modeladmin, request, queryset):
    type_1 = RubbishDistrict.objects.get(city_type="gmina", rubbish_type__name="wielkogabarytowe i zużyty sprzęt elektryczny i elektroniczny")

    for obj in queryset:
        obj.rubbish_district.add(type_1)

add_big_rubbish_district_1.short_description = "Odpady wielkogabarytowe - gmina"

class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "street",
        "city",
        "all_rubbish_districts_for_address",
        "status_rubbish_districts",
        "status_city_type_in_rubbish_district",
    )
    search_fields = (
        "city__name",
        "street__name",
        "status_rubbish_districts",
        "status_city_type_in_rubbish_district",
    )
    ordering = ("city", "street")
    autocomplete_fields = ("city", "street")
    filter_horizontal = ("rubbish_district",)
    list_filter = (
        "city",
        "rubbish_district__city_type",
    )
    actions = [add_big_rubbish_district_1]

    fieldsets = [
        ("Adres", {"fields": ["city", "street"]}),
        ("Rejon", {"fields": ["rubbish_district"]}),
    ]

    def all_rubbish_districts_for_address(self, obj):
        rubbish_district_all = obj.rubbish_district
        if rubbish_district_all.exists():
            rubbish_district_all = (
                rubbish_district_all.select_related("rubbish_type")
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
    try:
        RubbishType.objects.count()
    except ProgrammingError:
        all_rubbish_districts_for_address.short_description = format_html(
            f"Przypisane rejony"
        )
    else:
        all_rubbish_districts_for_address.short_description = format_html(
            f"Przypisane rejony<br>(docelowo: {RubbishType.objects.count()})"
        )

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
            .annotate(
                distinct_count_rubbish_type=Count(
                    "rubbish_district__rubbish_type__name", distinct=True
                )
            )
            .annotate(
                status_rubbish_districts=Case(
                    When(
                        Q(count_rubbish_districts=0),
                        then=False,
                    ),
                    When(
                        Q(count_rubbish_districts=count_rubbish_types)
                        & ~Q(
                            distinct_count_rubbish_type__lt=F("count_rubbish_districts")
                        ),
                        then=True,
                    ),
                    When(
                        Q(count_rubbish_districts=count_rubbish_types)
                        & Q(
                            distinct_count_rubbish_type__lt=F("count_rubbish_districts")
                        ),
                        then=False,
                    ),
                    When(
                        Q(count_rubbish_districts__lt=count_rubbish_types)
                        & Q(count_rubbish_districts__gt=0),
                        then=False,
                    ),
                    When(
                        Q(count_rubbish_districts__gt=count_rubbish_types), then=False,
                    ),
                    output_field=BooleanField(),
                )
            )
            .annotate(
                status_city_type_in_rubbish_district=Case(
                    When(~Q(errors_in_rubbish_districts_city_type=0), then=False),
                    When(
                        Q(errors_in_rubbish_districts_city_type=0)
                        & Q(distinct_count_rubbish_type__gte=1),
                        then=True,
                    ),
                    output_field=BooleanField(),
                )
            )
            .select_related("city", "street")
            .prefetch_related("rubbish_district")
        )

    def status_rubbish_districts(self, obj):
        return obj.status_rubbish_districts

    status_rubbish_districts.boolean = True
    status_rubbish_districts.short_description = format_html("Rejony<br>(status)")
    status_rubbish_districts.admin_order_field = "status_rubbish_districts"

    def status_city_type_in_rubbish_district(self, obj):
        return obj.status_city_type_in_rubbish_district

    status_city_type_in_rubbish_district.boolean = True
    status_city_type_in_rubbish_district.short_description = format_html(
        "Typ miejscowości<br>(status)"
    )
    status_city_type_in_rubbish_district.admin_order_field = (
        "status_city_type_in_rubbish_district"
    )


admin.site.register(Street, StreetAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Address, AddressAdmin)
