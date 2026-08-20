from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from stocks.models import Stock


class WatchlistTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("watcher", password="safe-password-123")
        self.stock = Stock.objects.create(symbol="WATCH", company_name="Watch Limited", sector="Test", current_price=Decimal("100"), previous_close=100, open_price=100, high_price=100, low_price=100)
        self.client = APIClient(); self.client.force_authenticate(self.user)

    def test_user_can_add_and_remove_watchlist_item(self):
        created = self.client.post("/api/watchlist/", {"stock": self.stock.id}, format="json")
        self.assertEqual(created.status_code, 201)
        listed = self.client.get("/api/watchlist/")
        self.assertEqual(listed.json()["count"], 1)
        self.assertEqual(self.client.delete(f"/api/watchlist/{created.json()['id']}/").status_code, 204)
