from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

from stocks.models import HistoricalStockPrice, Stock


STOCKS = [
    ("NABIL", "Nabil Bank Limited", "Commercial Bank", "523.00", "515.00", 138500, "72455500.00"),
    ("NICA", "NIC Asia Bank Limited", "Commercial Bank", "817.00", "802.00", 96800, "79085600.00"),
    ("ADBL", "Agricultural Development Bank Limited", "Commercial Bank", "302.50", "307.00", 112400, "34001000.00"),
    ("SHIVM", "Shivam Cements Limited", "Manufacturing", "548.00", "536.00", 89100, "48826800.00"),
    ("HDL", "Himalayan Distillery Limited", "Manufacturing", "2140.00", "2102.00", 23900, "51146000.00"),
    ("NRIC", "Nepal Reinsurance Company Limited", "Insurance", "792.00", "804.00", 76400, "60508800.00"),
]


class Command(BaseCommand):
    help = "Create or update demo NEPSE stocks and 90 days of historical prices."

    def handle(self, *args, **options):
        today = timezone.localdate()
        for index, (symbol, company_name, sector, price, previous, volume, turnover) in enumerate(STOCKS):
            current = Decimal(price)
            previous_close = Decimal(previous)
            stock, _ = Stock.objects.update_or_create(
                symbol=symbol,
                defaults={
                    "company_name": company_name, "sector": sector, "current_price": current,
                    "previous_close": previous_close, "open_price": previous_close, "high_price": current + Decimal("5.00"),
                    "low_price": previous_close - Decimal("3.00"), "volume": volume, "turnover": Decimal(turnover),
                    "percentage_change": ((current - previous_close) / previous_close * 100).quantize(Decimal(".01")),
                    "listed_shares": 100000000 + index * 10000000, "market_cap": current * (100000000 + index * 10000000),
                },
            )
            for day in range(90):
                date = today - timedelta(days=89 - day)
                close = current - Decimal(89 - day) * Decimal("0.25") + Decimal((day + index) % 5 - 2)
                HistoricalStockPrice.objects.update_or_create(
                    stock=stock, date=date,
                    defaults={"open": close - Decimal("1.00"), "high": close + Decimal("3.00"), "low": close - Decimal("3.00"), "close": close, "volume": volume + day * 100, "turnover": close * (volume + day * 100)},
                )
        self.stdout.write(self.style.SUCCESS("Demo stocks seeded."))
