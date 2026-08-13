from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse


class StockApiTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo_stocks")

    def test_lists_and_searches_demo_stocks(self):
        response = self.client.get(reverse("stock-list"), {"search": "Nabil"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(response.json()["results"][0]["symbol"], "NABIL")

    def test_returns_stock_history_for_a_valid_range(self):
        response = self.client.get(reverse("stock-history", kwargs={"symbol": "NABIL"}), {"range": "7D"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["symbol"], "NABIL")
        self.assertGreaterEqual(len(response.json()["results"]), 7)

    def test_rejects_unknown_history_ranges(self):
        response = self.client.get(reverse("stock-history", kwargs={"symbol": "NABIL"}), {"range": "FOREVER"})
        self.assertEqual(response.status_code, 400)
