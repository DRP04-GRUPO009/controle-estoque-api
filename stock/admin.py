from django.contrib import admin

from stock.models import Stock, StockItem

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['school_unit']

@admin.register(StockItem)
class StockItemAdmin(admin.ModelAdmin):
    list_display = ['stock', 'product', 'quantity']
