from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import City, Street, Address
from schedule.models import RubbishType


# Register your models here.
class CityAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    ordering = ("name",)


class StreetAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    ordering = ("name",)


class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "street",
        "city",
        "get_rubbish_type_district",
        "rubbish_district_status",
    )
    search_fields = ("city__name", "street__name")
    ordering = ("city", "street")
    autocomplete_fields = ("city", "street")
    filter_horizontal = ("rubbish_district",)
    list_filter = (
        "rubbish_district__name",
        "rubbish_district__city_type",
        "city",
        "street",
    )

    fieldsets = [
        ("Adres", {"fields": ["city", "street"]}),
        ("Rejon", {"fields": ["rubbish_district"]}),
    ]

    def get_rubbish_type_district(self, obj):
        return mark_safe(
            " | ".join(
                f"<b>{district.rubbish_type}</b> - {district.name} ({district.city_type.capitalize()})"
                for district in obj.rubbish_district.all()
                .order_by("rubbish_type")
                .select_related("rubbish_type")
            )
        )

    get_rubbish_type_district.short_description = "Przypisane rejony"

    def rubbish_district_status(self, obj):
        count_districts = obj.rubbish_district.count()
        count_rubbish_types = RubbishType.objects.count()
        if count_districts == count_rubbish_types:
            city_type = obj.city.city_type
            error_in_city_type = []
            for district in obj.rubbish_district.all():
                if district.city_type != city_type:
                    error_in_city_type.append(district.rubbish_type)

            if len(error_in_city_type) == 0:
                return mark_safe(
                    f"<span style='color:green'>Liczba zdefiniowanych rejonów: {count_districts}</style>"
                )
            else:
                error_message = [
                    ", ".join(rubbish_type.name for rubbish_type in error_in_city_type)
                ]
                return mark_safe(
                    f"<span style='color:red'><b>Błąd</b>: {error_message[0]}</span>"
                )

        if count_districts < count_rubbish_types:
            return mark_safe(
                f"<span style='color:red'>Liczba zdefiniowanych rejonów: {count_districts} (za mało)</style>"
            )
        else:
            return mark_safe(
                f"<span style='color:red'>Liczba zdefiniowanych rejonów: {count_districts} (za dużo)</style>"
            )

    rubbish_district_status.short_description = "Status"


admin.site.register(Street, StreetAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Address, AddressAdmin)
