from rest_framework import serializers
from .models import Broker, FloorSheet
class BrokerSerializer(serializers.ModelSerializer):
    class Meta: model = Broker; fields = "__all__"
class FloorSheetSerializer(serializers.ModelSerializer):
    symbol = serializers.CharField(source="stock.symbol", read_only=True)
    buyer = BrokerSerializer(source="buyer_broker", read_only=True); seller = BrokerSerializer(source="seller_broker", read_only=True)
    class Meta: model = FloorSheet; fields = "__all__"
