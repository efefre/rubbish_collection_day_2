from django.contrib import admin
from .models import WebPage
# Register your models here.


class WebPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'publish', 'status')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('status',)


admin.site.register(WebPage, WebPageAdmin)
