from rest_framework import serializers

from .models import HistoricalStockPrice, Stock


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ("id", "symbol", "company_name", "sector", "current_price", "previous_close", "open_price", "high_price", "low_price", "volume", "turnover", "percentage_change", "listed_shares", "market_cap", "updated_at")


class HistoricalStockPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalStockPrice
        fields = ("date", "open", "high", "low", "close", "volume", "turnover")

