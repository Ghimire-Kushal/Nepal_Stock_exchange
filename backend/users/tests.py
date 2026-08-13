from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient


class HealthCheckTests(TestCase):
    def test_health_check_returns_service_status(self):
        response = self.client.get(reverse("health-check"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"status": "ok", "service": "nepse-analysis-api"},
        )

    def test_health_check_allows_the_development_frontend_origin(self):
        response = self.client.get(
            reverse("health-check"),
            HTTP_ORIGIN="http://localhost:5174",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Access-Control-Allow-Origin"], "http://localhost:5174")


class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "username": "sita",
            "email": "sita@example.com",
            "password": "secure-pass-123",
            "first_name": "Sita",
            "last_name": "Shrestha",
        }

    def test_user_can_register_login_and_manage_profile(self):
        registration = self.client.post(reverse("register"), self.user_data, format="json")
        self.assertEqual(registration.status_code, 201)
        self.assertNotIn("password", registration.json())

        login = self.client.post(
            reverse("login"),
            {"username": self.user_data["username"], "password": self.user_data["password"]},
            format="json",
        )
        self.assertEqual(login.status_code, 200)
        self.assertIn("access", login.json())
        self.assertIn("refresh", login.json())

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.json()['access']}")
        profile = self.client.get(reverse("profile"))
        self.assertEqual(profile.status_code, 200)
        self.assertEqual(profile.json()["email"], self.user_data["email"])

        updated_profile = self.client.put(
            reverse("profile"),
            {"email": "sita.shrestha@example.com", "first_name": "Sita", "last_name": "Karki"},
            format="json",
        )
        self.assertEqual(updated_profile.status_code, 200)
        self.assertEqual(updated_profile.json()["last_name"], "Karki")

    def test_profile_requires_authentication(self):
        self.assertEqual(self.client.get(reverse("profile")).status_code, 401)
