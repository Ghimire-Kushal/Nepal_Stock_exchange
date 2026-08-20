from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from stocks.models import Stock
from .services import DemoDataProvider
@api_view(["GET"])
@permission_classes([AllowAny])
def dashboard(request):
    data=DemoDataProvider().get_market_summary(); stocks=Stock.objects.all()
    data.update({"top_gainers": list(stocks.order_by("-percentage_change").values("symbol","company_name","current_price","percentage_change")[:5]),"top_losers":list(stocks.order_by("percentage_change").values("symbol","company_name","current_price","percentage_change")[:5]),"top_turnover":list(stocks.order_by("-turnover").values("symbol","turnover","current_price")[:5]),"top_volume":list(stocks.order_by("-volume").values("symbol","volume","current_price")[:5])})
    return Response(data)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def system_statistics(request):
    """Small protected dashboard for administrators; no market-data provider required."""
    from django.contrib.auth import get_user_model
    from brokers.models import Broker, FloorSheet
    from portfolio.models import Portfolio
    from trading.models import PaperTrade
    from watchlist.models import Watchlist

    return Response({
        "users": get_user_model().objects.count(),
        "stocks": Stock.objects.count(),
        "brokers": Broker.objects.count(),
        "floorsheet_transactions": FloorSheet.objects.count(),
        "portfolios": Portfolio.objects.count(),
        "watchlist_items": Watchlist.objects.count(),
        "paper_trades": PaperTrade.objects.count(),
    })
