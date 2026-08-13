from django.db import transaction
from rest_framework import generics, permissions, serializers
from rest_framework.response import Response
from .models import PaperWallet, PaperHolding, PaperTrade
class TradeSerializer(serializers.ModelSerializer):
    symbol=serializers.CharField(source="stock.symbol",read_only=True)
    class Meta: model=PaperTrade; fields=("id","stock","symbol","trade_type","quantity","price","total_amount","status","created_at"); read_only_fields=("total_amount","status")
    def validate(self,d):
        if d["quantity"] <= 0 or d["price"] <= 0: raise serializers.ValidationError("Quantity and price must be positive.")
        return d
class TradeView(generics.ListCreateAPIView):
    serializer_class=TradeSerializer; permission_classes=(permissions.IsAuthenticated,)
    def get_queryset(self): return PaperTrade.objects.filter(user=self.request.user).select_related("stock")
    @transaction.atomic
    def perform_create(self, serializer):
        user=self.request.user; wallet,_=PaperWallet.objects.select_for_update().get_or_create(user=user); stock=serializer.validated_data["stock"]; qty=serializer.validated_data["quantity"]; price=serializer.validated_data["price"]; total=qty*price; typ=serializer.validated_data["trade_type"]; holding,_=PaperHolding.objects.select_for_update().get_or_create(user=user,stock=stock)
        if typ == "BUY":
            if wallet.balance < total: raise serializers.ValidationError({"balance":"Insufficient virtual balance."})
            holding.average_buy_price=((holding.quantity*holding.average_buy_price)+total)/(holding.quantity+qty); holding.quantity += qty; wallet.balance -= total
        else:
            if holding.quantity < qty: raise serializers.ValidationError({"quantity":"Cannot sell more shares than owned."})
            holding.quantity -= qty; wallet.balance += total
        holding.save(); wallet.save(); serializer.save(user=user,total_amount=total)
class TradingSummary(generics.GenericAPIView):
    permission_classes=(permissions.IsAuthenticated,)
    def get(self,request):
        wallet,_=PaperWallet.objects.get_or_create(user=request.user); hs=PaperHolding.objects.filter(user=request.user).select_related("stock"); value=sum((x.quantity*x.stock.current_price for x in hs),0); trades=PaperTrade.objects.filter(user=request.user); wins=trades.filter(trade_type="SELL",price__gt=0).count()
        return Response({"virtual_balance":wallet.balance,"portfolio_value":value,"total_value":wallet.balance+value,"number_of_trades":trades.count(),"win_rate":round(wins/trades.filter(trade_type="SELL").count()*100,2) if trades.filter(trade_type="SELL").exists() else 0,"holdings":[{"symbol":x.stock.symbol,"quantity":x.quantity,"current_value":x.quantity*x.stock.current_price} for x in hs]})
