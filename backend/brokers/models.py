from django.db import models
from stocks.models import Stock

class Broker(models.Model):
    broker_number = models.PositiveIntegerField(unique=True, db_index=True)
    broker_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    website = models.URLField(blank=True)
    class Meta: ordering = ("broker_number",)
    def __str__(self): return f"{self.broker_number} - {self.broker_name}"

class FloorSheet(models.Model):
    contract_number = models.CharField(max_length=64, unique=True)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="floorsheets")
    buyer_broker = models.ForeignKey(Broker, on_delete=models.PROTECT, related_name="purchases")
    seller_broker = models.ForeignKey(Broker, on_delete=models.PROTECT, related_name="sales")
    quantity = models.PositiveIntegerField()
    rate = models.DecimalField(max_digits=12, decimal_places=2)
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    trade_date = models.DateField(db_index=True)
    trade_time = models.TimeField(null=True, blank=True)
    class Meta:
        ordering = ("-trade_date", "contract_number")
        indexes = [models.Index(fields=("stock", "trade_date")), models.Index(fields=("buyer_broker", "trade_date")), models.Index(fields=("seller_broker", "trade_date"))]
