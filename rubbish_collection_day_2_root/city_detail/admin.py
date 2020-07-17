from django.contrib import admin
from django.utils.html import format_html
from .models import City, Street, Address
from schedule.models import RubbishType
from django.db.models import Case, Value, When, CharField, Count, Q, F
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
        # "rubbish_district_status",
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
                " | ".join(
                    f"<b>{district.rubbish_type}</b> - {district.name} ({district.city_type.capitalize()})"
                    if district.rubbish_type.name not in counter_rubbish_types
                    else f"<span style='color: red'><b>{district.rubbish_type}</b> - {district.name} ({district.city_type.capitalize()})</span>"
                    for district in rubbish_district_all
                )
            )
        else:
            return format_html(
                " | ".join(
                    f"<b>{district.rubbish_type}</b> - {district.name} ({district.city_type.capitalize()})"
                    if district.city_type == obj.city.city_type
                    else f"<span style='color: red'><b>{district.rubbish_type}</b> - {district.name} ({district.city_type.capitalize()})</span>"
                    for district in rubbish_district_all
                )
            )

    all_rubbish_districts_for_address.short_description = "Przypisane rejony"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("city", "street")

    # def get_queryset(self, request):
    #     count_rubbish_types = RubbishType.objects.count()

    #     return (
    #         super()
    #         .get_queryset(request)
    #         .annotate(count_rubbish_districts=Count("rubbish_district"))
    #         .annotate(
    #             errors_in_rubbish_districts_city_type=Count(
    #                 Case(
    #                     When(
    #                         ~Q(rubbish_district__city_type=F("city__city_type")),
    #                         then=F("rubbish_district__city_type"),
    #                     ),
    #                     output_field=CharField(),
    #                 )
    #             )
    #         )
    #         .annotate(
    #             status_for_filter=Case(
    #                 When(
    #                     ~Q(count_rubbish_districts=count_rubbish_types),
    #                     then=Value("err_in_dis"),
    #                 ),
    #                 When(
    #                     ~Q(errors_in_rubbish_districts_city_type=0),
    #                     then=Value("err_in_cit_typ"),
    #                 ),
    #                 output_field=CharField(),
    #             )
    #         )
    #     )

    # def status_for_filter(self, obj):
    #     return obj.status_for_filter

    # def rubbish_district_status(self, obj):
    #     count_districts = obj.count_rubbish_districts
    #     count_rubbish_types = RubbishType.objects.count()
    #     if count_districts == count_rubbish_types:
    #         error_in_city_type = []
    #         city_type = obj.city.city_type
    #         for district in obj.rubbish_district.all():
    #             if district.city_type != city_type:
    #                 error_in_city_type.append(district.rubbish_type)

    #         if len(error_in_city_type) == 0:
    #             return mark_safe(
    #                 f"<span style='color:green'>Liczba zdefiniowanych rejonów: {count_districts}</style>"
    #             )
    #         else:
    #             error_message = [
    #                 ", ".join(rubbish_type.name for rubbish_type in error_in_city_type)
    #             ]
    #             return mark_safe(
    #                 f"<span style='color:red'><b>Błąd</b>: {error_message[0]}</span>"
    #             )

    #     if count_districts < count_rubbish_types:
    #         return mark_safe(
    #             f"<span style='color:red'>Liczba zdefiniowanych rejonów: {count_districts} (za mało)</style>"
    #         )
    #     else:
    #         return mark_safe(
    #             f"<span style='color:red'>Liczba zdefiniowanych rejonów: {count_districts} (za dużo)</style>"
    #         )

    # rubbish_district_status.short_description = "Status"


admin.site.register(Street, StreetAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Address, AddressAdmin)
