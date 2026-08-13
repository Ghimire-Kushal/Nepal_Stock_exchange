from rest_framework import generics, permissions
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from .models import Watchlist
class WatchSerializer(ModelSerializer):
    symbol = __import__('rest_framework').serializers.CharField(source="stock.symbol", read_only=True); current_price = __import__('rest_framework').serializers.DecimalField(source="stock.current_price", max_digits=12, decimal_places=2, read_only=True); percentage_change = __import__('rest_framework').serializers.DecimalField(source="stock.percentage_change", max_digits=7, decimal_places=2, read_only=True)
    class Meta: model=Watchlist; fields=("id","stock","symbol","current_price","percentage_change","created_at")
class WatchlistView(generics.ListCreateAPIView):
    serializer_class=WatchSerializer; permission_classes=(permissions.IsAuthenticated,)
    def get_queryset(self): return Watchlist.objects.filter(user=self.request.user).select_related("stock")
    def perform_create(self, serializer): serializer.save(user=self.request.user)
class WatchDetail(generics.DestroyAPIView):
    serializer_class=WatchSerializer; permission_classes=(permissions.IsAuthenticated,)
    def get_queryset(self): return Watchlist.objects.filter(user=self.request.user)
