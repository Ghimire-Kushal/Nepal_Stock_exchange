from rest_framework import serializers
from .models import Portfolio, Holding
class HoldingSerializer(serializers.ModelSerializer):
    symbol = serializers.CharField(source="stock.symbol", read_only=True); company_name = serializers.CharField(source="stock.company_name", read_only=True); current_price = serializers.DecimalField(source="stock.current_price", max_digits=12, decimal_places=2, read_only=True)
    current_value = serializers.SerializerMethodField(); profit_loss = serializers.SerializerMethodField(); return_percent = serializers.SerializerMethodField()
    class Meta: model = Holding; fields = ("id", "portfolio", "stock", "symbol", "company_name", "quantity", "average_buy_price", "total_investment", "current_price", "current_value", "profit_loss", "return_percent") ; read_only_fields = ("portfolio", "total_investment")
    def get_current_value(self, x): return x.quantity * x.stock.current_price
    def get_profit_loss(self, x): return self.get_current_value(x) - x.total_investment
    def get_return_percent(self, x): return round(float(self.get_profit_loss(x) / x.total_investment * 100), 2) if x.total_investment else 0
class PortfolioSerializer(serializers.ModelSerializer):
    holdings = HoldingSerializer(many=True, read_only=True)
    class Meta: model = Portfolio; fields = ("id", "name", "created_at", "holdings")
