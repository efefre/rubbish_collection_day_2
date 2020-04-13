from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import City, Street, Address


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
        "count_rubbish_district",
    )
    search_fields = ("city__name", "street__name")
    ordering = ("city", "street")
    autocomplete_fields = ("city", "street")
    filter_horizontal = ("rubbish_district",)
    list_filter = (
        "rubbish_district__rubbish_type",
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
                for district in obj.rubbish_district.all().order_by("rubbish_type")
            )
        )

    get_rubbish_type_district.short_description = "Przypisane rejony"

    def count_rubbish_district(self, obj):
        return obj.rubbish_district.count()

    count_rubbish_district.short_description = "Liczba rejonów"


admin.site.register(Street, StreetAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Address, AddressAdmin)
