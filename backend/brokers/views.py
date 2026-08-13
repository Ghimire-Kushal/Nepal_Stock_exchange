import csv
from decimal import Decimal
from django.db.models import Sum
from django.utils.dateparse import parse_date
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Broker, FloorSheet
from .serializers import BrokerSerializer, FloorSheetSerializer
from stocks.models import Stock

class BrokerList(generics.ListAPIView):
    queryset = Broker.objects.all(); serializer_class = BrokerSerializer; permission_classes = (permissions.AllowAny,)
class BrokerDetail(generics.RetrieveAPIView):
    queryset = Broker.objects.all(); serializer_class = BrokerSerializer; permission_classes = (permissions.AllowAny,); lookup_field = "broker_number"
class FloorSheetList(generics.ListAPIView):
    serializer_class = FloorSheetSerializer; permission_classes = (permissions.AllowAny,)
    def get_queryset(self):
        q = FloorSheet.objects.select_related("stock", "buyer_broker", "seller_broker")
        if s := self.request.query_params.get("symbol"): q = q.filter(stock__symbol=s.upper())
        if b := self.request.query_params.get("broker"): q = q.filter(buyer_broker__broker_number=b) | q.filter(seller_broker__broker_number=b)
        return q
@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def broker_activity(request, broker_number):
    broker = generics.get_object_or_404(Broker, broker_number=broker_number)
    buy = FloorSheet.objects.filter(buyer_broker=broker).values("stock__symbol").annotate(quantity=Sum("quantity"), amount=Sum("amount")).order_by("-amount")[:10]
    sell = FloorSheet.objects.filter(seller_broker=broker).values("stock__symbol").annotate(quantity=Sum("quantity"), amount=Sum("amount")).order_by("-amount")[:10]
    return Response({"broker": BrokerSerializer(broker).data, "most_bought": list(buy), "most_sold": list(sell)})
@api_view(["POST"])
@permission_classes([permissions.IsAdminUser])
def import_floorsheet(request):
    file = request.FILES.get("file")
    if not file or file.size > 5 * 1024 * 1024: return Response({"error": "Provide a CSV file no larger than 5 MB."}, status=400)
    try: rows = list(csv.DictReader(file.read().decode("utf-8-sig").splitlines()))
    except UnicodeDecodeError: return Response({"error": "CSV must be UTF-8 encoded."}, status=400)
    required = {"contract_number", "symbol", "buyer_broker", "seller_broker", "quantity", "rate", "amount", "trade_date"}
    if not rows or not required.issubset(rows[0]): return Response({"error": "CSV columns are invalid."}, status=400)
    created = 0
    for row in rows:
        if FloorSheet.objects.filter(contract_number=row["contract_number"]).exists(): continue
        try:
            stock = Stock.objects.get(symbol=row["symbol"].upper()); buyer = Broker.objects.get(broker_number=row["buyer_broker"]); seller = Broker.objects.get(broker_number=row["seller_broker"])
            FloorSheet.objects.create(contract_number=row["contract_number"], stock=stock, buyer_broker=buyer, seller_broker=seller, quantity=int(row["quantity"]), rate=Decimal(row["rate"]), amount=Decimal(row["amount"]), trade_date=parse_date(row["trade_date"])); created += 1
        except (Stock.DoesNotExist, Broker.DoesNotExist, ValueError, TypeError): return Response({"error": f"Invalid row for contract {row.get('contract_number')}"}, status=400)
    return Response({"created": created, "skipped_duplicates": len(rows)-created}, status=status.HTTP_201_CREATED)
