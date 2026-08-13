from decimal import Decimal
from django.conf import settings
from django.db import models
from stocks.models import Stock
class PaperWallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="paper_wallet")
    balance = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal("1000000.00"))
class PaperHolding(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="paper_holdings")
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE); quantity=models.PositiveIntegerField(default=0); average_buy_price=models.DecimalField(max_digits=12, decimal_places=2, default=0)
    class Meta: unique_together=("user","stock")
class PaperTrade(models.Model):
    BUY="BUY"; SELL="SELL"; TYPES=((BUY,"Buy"),(SELL,"Sell"))
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="paper_trades"); stock=models.ForeignKey(Stock,on_delete=models.PROTECT); trade_type=models.CharField(max_length=4,choices=TYPES); quantity=models.PositiveIntegerField(); price=models.DecimalField(max_digits=12,decimal_places=2); total_amount=models.DecimalField(max_digits=18,decimal_places=2); status=models.CharField(max_length=20,default="EXECUTED"); created_at=models.DateTimeField(auto_now_add=True)
