import csv
from decimal import Decimal
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from stocks.models import Stock


class Command(BaseCommand):
    help = "Import a manually downloaded NEPSE Listed Securities CSV without scraping NEPSE."

    def add_arguments(self, parser):
        parser.add_argument("csv_path", type=Path)

    def handle(self, *args, **options):
        path = options["csv_path"]
        if not path.is_file():
            raise CommandError(f"CSV file not found: {path}")
        with path.open(encoding="utf-8-sig", newline="") as source:
            rows = [{str(k).strip().lower(): (v or "").strip() for k, v in row.items()} for row in csv.DictReader(source)]
        if not rows or not all(row.get("symbol") and (row.get("name") or row.get("company_name")) for row in rows):
            raise CommandError("CSV requires symbol plus name or company_name columns.")
        created = updated = 0
        for row in rows:
            defaults = {"company_name": row.get("name") or row.get("company_name"), "sector": row.get("sector") or "Unclassified"}
            stock, was_created = Stock.objects.get_or_create(
                symbol=row["symbol"].upper(),
                defaults={**defaults, "current_price": Decimal("0"), "previous_close": Decimal("0"), "open_price": Decimal("0"), "high_price": Decimal("0"), "low_price": Decimal("0")},
            )
            if was_created: created += 1
            else:
                stock.company_name, stock.sector = defaults["company_name"], defaults["sector"]
                stock.save(update_fields=("company_name", "sector", "updated_at")); updated += 1
        self.stdout.write(self.style.SUCCESS(f"Imported NEPSE company list: {created} created, {updated} updated."))
