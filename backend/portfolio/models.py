from django.conf import settings
from django.db import models
from stocks.models import Stock
class Portfolio(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="portfolios")
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: unique_together = ("user", "name")
class Holding(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name="holdings")
    stock = models.ForeignKey(Stock, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    average_buy_price = models.DecimalField(max_digits=12, decimal_places=2)
    total_investment = models.DecimalField(max_digits=18, decimal_places=2, editable=False)
    created_at = models.DateTimeField(auto_now_add=True); updated_at = models.DateTimeField(auto_now=True)
    class Meta: unique_together = ("portfolio", "stock")
    def save(self, *args, **kwargs): self.total_investment = self.quantity * self.average_buy_price; super().save(*args, **kwargs)
