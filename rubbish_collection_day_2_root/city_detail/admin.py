from django.contrib import admin
from .models import City, Street, Address


# Register your models here.
class CityAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    ordering = ("name",)


class StreetAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    ordering = ("name",)


class AddressAdmin(admin.ModelAdmin):
    search_fields = ("city__name", "street__name")
    ordering = ("city", "street")


admin.site.register(Street, StreetAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Address, AddressAdmin)
