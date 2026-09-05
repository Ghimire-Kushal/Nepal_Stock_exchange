import csv
from decimal import Decimal, InvalidOperation
from django.db.models import Sum
from django.utils.dateparse import parse_date
from django.db import transaction
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
    stock_fields = ("stock__symbol", "stock__company_name", "stock__sector", "stock__current_price", "stock__percentage_change")
    buy = FloorSheet.objects.filter(buyer_broker=broker).values(*stock_fields).annotate(quantity=Sum("quantity"), amount=Sum("amount")).order_by("-amount")
    sell = FloorSheet.objects.filter(seller_broker=broker).values(*stock_fields).annotate(quantity=Sum("quantity"), amount=Sum("amount")).order_by("-amount")

    def normalize(rows):
        return [{
            "symbol": row["stock__symbol"], "company_name": row["stock__company_name"],
            "sector": row["stock__sector"], "current_price": row["stock__current_price"],
            "percentage_change": row["stock__percentage_change"], "quantity": row["quantity"],
            "amount": row["amount"], "average_price": round(float(row["amount"] / row["quantity"]), 2) if row["quantity"] else 0,
        } for row in rows]

    bought, sold = normalize(buy), normalize(sell)
    activity = {}
    for direction, rows in (("buy", bought), ("sell", sold)):
        for row in rows:
            item = activity.setdefault(row["symbol"], {**{key: row[key] for key in ("symbol", "company_name", "sector", "current_price", "percentage_change")}, "buy_quantity": 0, "buy_amount": 0, "buy_average_price": 0, "sell_quantity": 0, "sell_amount": 0, "sell_average_price": 0})
            item[f"{direction}_quantity"] = row["quantity"]
            item[f"{direction}_amount"] = row["amount"]
            item[f"{direction}_average_price"] = row["average_price"]
    all_stock_activity = []
    for item in activity.values():
        item["net_quantity"] = item["buy_quantity"] - item["sell_quantity"]
        item["net_amount"] = item["buy_amount"] - item["sell_amount"]
        all_stock_activity.append(item)
    all_stock_activity.sort(key=lambda item: abs(item["buy_amount"]) + abs(item["sell_amount"]), reverse=True)
    summary = {
        "stocks_traded": len(all_stock_activity), "total_buy_quantity": sum(row["quantity"] for row in bought),
        "total_sell_quantity": sum(row["quantity"] for row in sold), "total_buy_amount": sum((row["amount"] for row in bought), Decimal("0")),
        "total_sell_amount": sum((row["amount"] for row in sold), Decimal("0")),
    }
    summary["total_turnover"] = summary["total_buy_amount"] + summary["total_sell_amount"]
    return Response({"broker": BrokerSerializer(broker).data, "summary": summary, "most_bought": bought[:10], "most_sold": sold[:10], "all_stock_activity": all_stock_activity})
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
    try:
        with transaction.atomic():
            for row in rows:
                if FloorSheet.objects.filter(contract_number=row["contract_number"]).exists(): continue
                trade_date = parse_date(row["trade_date"])
                if not trade_date: raise ValueError("invalid date")
                stock = Stock.objects.get(symbol=row["symbol"].upper()); buyer = Broker.objects.get(broker_number=row["buyer_broker"]); seller = Broker.objects.get(broker_number=row["seller_broker"])
                quantity, rate, amount = int(row["quantity"]), Decimal(row["rate"]), Decimal(row["amount"])
                if quantity <= 0 or rate <= 0 or amount <= 0: raise ValueError("non-positive values")
                FloorSheet.objects.create(contract_number=row["contract_number"], stock=stock, buyer_broker=buyer, seller_broker=seller, quantity=quantity, rate=rate, amount=amount, trade_date=trade_date); created += 1
    except (Stock.DoesNotExist, Broker.DoesNotExist, ValueError, TypeError, InvalidOperation):
        return Response({"error": f"Invalid row for contract {row.get('contract_number')}"}, status=400)
    return Response({"created": created, "skipped_duplicates": len(rows)-created}, status=status.HTTP_201_CREATED)
