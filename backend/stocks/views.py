from datetime import timedelta

from django.db.models import Q
from django.utils import timezone
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Stock
from .serializers import HistoricalStockPriceSerializer, StockSerializer


class StockListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = StockSerializer

    def get_queryset(self):
        query = self.request.query_params.get("search", "").strip()
        stocks = Stock.objects.all()
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

