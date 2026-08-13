from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from stocks.models import Stock
from .services import DemoDataProvider
@api_view(["GET"])
@permission_classes([AllowAny])
def dashboard(request):
    data=DemoDataProvider().get_market_summary(); stocks=Stock.objects.all()
    data.update({"top_gainers": list(stocks.order_by("-percentage_change").values("symbol","company_name","current_price","percentage_change")[:5]),"top_losers":list(stocks.order_by("percentage_change").values("symbol","company_name","current_price","percentage_change")[:5]),"top_turnover":list(stocks.order_by("-turnover").values("symbol","turnover","current_price")[:5]),"top_volume":list(stocks.order_by("-volume").values("symbol","volume","current_price")[:5])})
    return Response(data)
