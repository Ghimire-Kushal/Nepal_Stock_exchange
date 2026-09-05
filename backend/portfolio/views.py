from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .models import Portfolio, Holding
from .serializers import PortfolioSerializer, HoldingSerializer
class PortfolioList(generics.ListCreateAPIView):
    serializer_class = PortfolioSerializer; permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self): return Portfolio.objects.filter(user=self.request.user).prefetch_related("holdings__stock")
    def perform_create(self, serializer): serializer.save(user=self.request.user)
class PortfolioDetail(generics.RetrieveDestroyAPIView):
    serializer_class = PortfolioSerializer; permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self): return Portfolio.objects.filter(user=self.request.user).prefetch_related("holdings__stock")
class HoldingDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HoldingSerializer; permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self): return Holding.objects.filter(portfolio__user=self.request.user).select_related("stock")
class HoldingCreate(generics.CreateAPIView):
    serializer_class = HoldingSerializer; permission_classes = (permissions.IsAuthenticated,)
    def perform_create(self, serializer):
        portfolio = get_object_or_404(Portfolio, pk=self.kwargs["portfolio_id"], user=self.request.user)
        serializer.save(portfolio=portfolio)
class PortfolioSummary(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        holdings = Holding.objects.filter(portfolio__user=request.user).select_related("stock")
        investment = sum((x.total_investment for x in holdings), 0); value = sum((x.quantity * x.stock.current_price for x in holdings), 0)
        sectors = {}
        for x in holdings: sectors[x.stock.sector] = sectors.get(x.stock.sector, 0) + float(x.quantity * x.stock.current_price)
        return Response({"total_investment": investment, "current_value": value, "profit_loss": value-investment, "return_percent": round(float((value-investment)/investment*100),2) if investment else 0, "sector_allocation": [{"name": k, "value": v} for k,v in sectors.items()]})
