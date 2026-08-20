from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient


class SystemStatisticsTests(TestCase):
    def test_statistics_are_admin_only(self):
        client = APIClient()
        self.assertEqual(client.get("/api/analytics/admin/statistics/").status_code, 401)
        admin = get_user_model().objects.create_superuser("admin", "admin@example.com", "safe-password-123")
        client.force_authenticate(admin)
        response = client.get("/api/analytics/admin/statistics/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("stocks", response.json())
