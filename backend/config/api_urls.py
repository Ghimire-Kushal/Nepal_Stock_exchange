from django.urls import include, path

from .views import health_check

urlpatterns = [
    path("health/", health_check, name="health-check"),
    path("auth/", include("users.urls")),
    path("stocks/", include("stocks.urls")),
]
