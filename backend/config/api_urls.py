from django.urls import include, path

from .views import health_check

urlpatterns = [
    path("health/", health_check, name="health-check"),
    path("auth/", include("users.urls")),
    path("stocks/", include("stocks.urls")),
    path("brokers/", include("brokers.urls")),
    path("floorsheet/", include("brokers.urls_floorsheet")),
    path("portfolio/", include("portfolio.urls")),
    path("watchlist/", include("watchlist.urls")),
    path("paper-trading/", include("trading.urls")),
    path("analytics/", include("analytics.urls")),
    path("admin/floorsheet/", include("brokers.urls_admin")),
]
