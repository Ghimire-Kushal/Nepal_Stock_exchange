from django.conf import settings
from django.db import models
from stocks.models import Stock
class Watchlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="watchlist")
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: unique_together = ("user", "stock")
