from django.contrib import admin
from .models import Printer, Check

class CheckAdmin(admin.ModelAdmin):
    list_filter = ('printer_id', 'status')

class PrinterAdmin(admin.ModelAdmin):
    list_filter = ('name', 'api_key', 'point_id')


admin.site.register(Printer, PrinterAdmin)
admin.site.register(Check, CheckAdmin)
