from django.core.management import call_command
from django.contrib.auth import get_user_model
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

    def test_company_import_is_admin_only_and_adds_stock(self):
        response = self.client.post(reverse("import-companies"), {})
        self.assertEqual(response.status_code, 401)

        admin = get_user_model().objects.create_superuser("admin", "admin@example.com", "safe-password-123")
        from rest_framework.test import APIClient
        client = APIClient()
        client.force_authenticate(user=admin)
        from django.core.files.uploadedfile import SimpleUploadedFile
        csv_file = SimpleUploadedFile("nepse-companies.csv", b"symbol,name,sector\nTEST,Test Company Limited,Finance\n", content_type="text/csv")
        response = client.post(reverse("import-companies"), {"file": csv_file})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["created"], 1)
