from django.contrib import admin
from .models import Printer, Check


@admin.register(Printer)
class PrinterAdmin(admin.ModelAdmin):
    list_display = ('name', 'api_key', 'check_type', 'point_id')
    list_display_links = ('name',)


@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    list_display = ("printer", 'type', 'status')
    list_display_links = ('printer',)
    search_fields = ('printer', 'type', 'status')
