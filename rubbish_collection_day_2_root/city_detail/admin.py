from django.contrib import admin
from .models import City, Street


# Register your models here.
class CityAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    ordering = ('name',)


class StreetAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    ordering = ('name',)


admin.site.register(Street, StreetAdmin)
admin.site.register(City, CityAdmin)