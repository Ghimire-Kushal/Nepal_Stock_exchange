from datetime import timedelta

from django.db.models import Q, Sum, F, DecimalField, ExpressionWrapper
from django.utils import timezone
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Stock
from .serializers import HistoricalStockPriceSerializer, StockSerializer
from brokers.models import FloorSheet
from analytics.services import indicators


class StockListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = StockSerializer

    def get_queryset(self):
        query = self.request.query_params.get("search", "").strip()
        stocks = Stock.objects.all()
        sector = self.request.query_params.get("sector", "").strip()
        if sector:
            stocks = stocks.filter(sector__iexact=sector)
        if query:
            stocks = stocks.filter(Q(symbol__icontains=query) | Q(company_name__icontains=query) | Q(sector__icontains=query))
        return stocks


class StockDetailView(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = StockSerializer
    queryset = Stock.objects.all()
    lookup_field = "symbol"


@api_view(["GET"])
@permission_classes([AllowAny])
def stock_history(request, symbol):
    periods = {"7D": 7, "1M": 31, "3M": 92, "6M": 183, "1Y": 366}
    selected_range = request.query_params.get("range", "1M").upper()
    if selected_range not in {*periods, "ALL"}:
        return Response({"range": ["Use 7D, 1M, 3M, 6M, 1Y, or ALL."]}, status=400)
    stock = generics.get_object_or_404(Stock, symbol=symbol.upper())
    prices = stock.history.all()
    if selected_range != "ALL":
        prices = prices.filter(date__gte=timezone.localdate() - timedelta(days=periods[selected_range]))
    return Response({"symbol": stock.symbol, "range": selected_range, "results": HistoricalStockPriceSerializer(prices, many=True).data})


@api_view(["GET"])
@permission_classes([AllowAny])
def broker_analysis(request, symbol):
    days = {"today": 1, "1week": 7, "1month": 31, "3month": 92, "6month": 183}
    period = request.query_params.get("period", "today").lower()
    if period not in days:
        return Response({"period": ["Use today, 1week, 1month, 3month, or 6month."]}, status=400)
    stock = generics.get_object_or_404(Stock, symbol=symbol.upper())
    qs = FloorSheet.objects.filter(stock=stock, trade_date__gte=timezone.localdate() - timedelta(days=days[period])).select_related("buyer_broker", "seller_broker")
    total = qs.aggregate(value=Sum("amount"))["value"] or 0
    def rows(field):
        grouped = qs.values(f"{field}__broker_number", f"{field}__broker_name").annotate(quantity=Sum("quantity"), amount=Sum("amount")).order_by("-quantity")
        return [{"broker_number": r[f"{field}__broker_number"], "broker_name": r[f"{field}__broker_name"], "quantity": r["quantity"], "amount": r["amount"], "average_price": round(float(r["amount"] / r["quantity"]), 2) if r["quantity"] else 0, "percentage": round(float(r["amount"] / total * 100), 2) if total else 0} for r in grouped]
    bought, sold = rows("buyer_broker"), rows("seller_broker")
    merged = {}
    for key, data, side in [("buy", bought, "buy"), ("sell", sold, "sell")]:
        for row in data:
            item = merged.setdefault(row["broker_number"], {"broker_number": row["broker_number"], "broker_name": row["broker_name"], "buy_quantity": 0, "sell_quantity": 0, "buy_amount": 0, "sell_amount": 0})
            item[f"{side}_quantity"], item[f"{side}_amount"] = row["quantity"], row["amount"]
    net = []
    for item in merged.values():
        item["net_quantity"] = item["buy_quantity"] - item["sell_quantity"]
        item["net_amount"] = item["buy_amount"] - item["sell_amount"]
        item["label"] = "Strong Accumulation" if item["net_quantity"] > 1000 else "Moderate Accumulation" if item["net_quantity"] > 0 else "Strong Distribution" if item["net_quantity"] < -1000 else "Moderate Distribution" if item["net_quantity"] < 0 else "Neutral"
        net.append(item)
    return Response({"symbol": stock.symbol, "period": period, "most_bought": bought[:10], "most_sold": sold[:10], "net_holding": sorted(net, key=lambda x: x["net_quantity"], reverse=True)})


@api_view(["GET"])
@permission_classes([AllowAny])
def technical_analysis(request, symbol):
    stock = generics.get_object_or_404(Stock, symbol=symbol.upper())
    return Response(indicators(stock))
