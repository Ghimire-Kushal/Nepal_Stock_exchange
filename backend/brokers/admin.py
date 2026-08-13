from django.contrib import admin
from .models import Broker, FloorSheet
admin.site.register(Broker)
@admin.register(FloorSheet)
class FloorSheetAdmin(admin.ModelAdmin):
    list_display=("contract_number","stock","buyer_broker","seller_broker","quantity","rate","trade_date"); list_filter=("trade_date","stock"); search_fields=("contract_number","stock__symbol")
