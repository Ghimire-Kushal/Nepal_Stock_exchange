from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from stocks.models import Stock
from .models import PaperHolding, PaperWallet


class PaperTradingTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("trader", password="safe-password-123")
        self.stock = Stock.objects.create(symbol="TEST", company_name="Test Limited", sector="Test", current_price=Decimal("100"), previous_close=100, open_price=100, high_price=100, low_price=100)
        self.client = APIClient(); self.client.force_authenticate(self.user)

    def test_buy_updates_wallet_and_holding(self):
        response = self.client.post("/api/paper-trading/", {"stock": self.stock.id, "trade_type": "BUY", "quantity": 10, "price": "100"}, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(PaperWallet.objects.get(user=self.user).balance, Decimal("999000"))
        self.assertEqual(PaperHolding.objects.get(user=self.user, stock=self.stock).quantity, 10)

    def test_cannot_sell_more_than_owned(self):
        response = self.client.post("/api/paper-trading/", {"stock": self.stock.id, "trade_type": "SELL", "quantity": 1, "price": "100"}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("quantity", response.json())
