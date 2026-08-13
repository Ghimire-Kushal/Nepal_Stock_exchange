from django.contrib import admin

from .models import HistoricalStockPrice, Stock


class HistoricalStockPriceInline(admin.TabularInline):
    model = HistoricalStockPrice
    extra = 0


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ("symbol", "company_name", "sector", "current_price", "percentage_change")
    search_fields = ("symbol", "company_name", "sector")
    list_filter = ("sector",)
    inlines = (HistoricalStockPriceInline,)
