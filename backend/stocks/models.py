from django.db import models


class Stock(models.Model):
    symbol = models.CharField(max_length=20, unique=True)
    company_name = models.CharField(max_length=255)
    sector = models.CharField(max_length=100)
    current_price = models.DecimalField(max_digits=12, decimal_places=2)
    previous_close = models.DecimalField(max_digits=12, decimal_places=2)
    open_price = models.DecimalField(max_digits=12, decimal_places=2)
    high_price = models.DecimalField(max_digits=12, decimal_places=2)
    low_price = models.DecimalField(max_digits=12, decimal_places=2)
    volume = models.PositiveBigIntegerField(default=0)
    turnover = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    percentage_change = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    listed_shares = models.PositiveBigIntegerField(default=0)
    market_cap = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("symbol",)

    def __str__(self):
        return self.symbol


class HistoricalStockPrice(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="history")
    date = models.DateField()
    open = models.DecimalField(max_digits=12, decimal_places=2)
    high = models.DecimalField(max_digits=12, decimal_places=2)
    low = models.DecimalField(max_digits=12, decimal_places=2)
    close = models.DecimalField(max_digits=12, decimal_places=2)
    volume = models.PositiveBigIntegerField(default=0)
    turnover = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    class Meta:
        ordering = ("date",)
        constraints = [models.UniqueConstraint(fields=("stock", "date"), name="unique_stock_history_date")]

