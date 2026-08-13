"""Replace generated demo broker labels with a curated local broker list."""
from django.core.management.base import BaseCommand

from brokers.models import Broker, FloorSheet


BROKERS = [
    (1, "Kumari Securities Private Limited"), (3, "Arun Securities (PVT) Ltd."),
    (4, "Opal Securities Investment (PVT) Ltd."), (5, "Market Securities & Exchange (PVT) Ltd."),
    (6, "Agrawal Securities (PVT) Ltd."), (7, "J.F. Securites (PVT) Ltd."),
    (8, "Ashutosh Brokerage & Securities (PVT) Ltd."), (10, "Pragyan Securities (PVT) Ltd."),
    (11, "Malla & Malla Stock Broking Company Pvt. Limited"), (13, "Thrive Brokerage House Pvt. Ltd"),
    (14, "Nepal Stock House (PVT) Ltd."), (16, "Primo Securities (PVT) Ltd."),
    (17, "ABC Securities Private Limited"), (18, "Sagarmatha Securities Private Limited"),
    (19, "Nepal Investment And Securities Trading Private Limited"), (20, "Sipla Securities Private Limited"),
    (21, "Midas Stock Broking Company Private Limited"), (22, "Siprabi Securities Pvt. Ltd."),
    (25, "Sweta Securities Private Limited"), (26, "Asian Securities Private Ltd."),
]


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
