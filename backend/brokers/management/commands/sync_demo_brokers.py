"""Replace generated demo broker labels with a curated local broker list."""
from django.core.management.base import BaseCommand

from brokers.models import Broker, FloorSheet
from brokers.catalog import BROKERS


class Command(BaseCommand):
    help = "Replace generated demo broker names with curated broker numbers and names."

    def handle(self, *args, **options):
        generated = list(Broker.objects.filter(broker_name__startswith="Demo Securities"))
        curated = [Broker.objects.update_or_create(
            broker_number=number,
            defaults={"broker_name": name, "address": "Kathmandu, Nepal", "phone": "01-5550000"},
        )[0] for number, name in BROKERS]

        curated_ids = {broker.id for broker in curated}
        obsolete = [broker for broker in generated if broker.id not in curated_ids]
        for index, broker in enumerate(obsolete):
            replacement = curated[index % len(curated)]
            FloorSheet.objects.filter(buyer_broker=broker).update(buyer_broker=replacement)
            FloorSheet.objects.filter(seller_broker=broker).update(seller_broker=replacement)
        Broker.objects.filter(id__in=[broker.id for broker in obsolete]).delete()
        self.stdout.write(self.style.SUCCESS(f"Synced {len(curated)} broker names."))
