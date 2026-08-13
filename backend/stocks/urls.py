from django.urls import path

from .views import StockDetailView, StockListView, stock_history

urlpatterns = [
    path("", StockListView.as_view(), name="stock-list"),
    path("<str:symbol>/", StockDetailView.as_view(), name="stock-detail"),
    path("<str:symbol>/history/", stock_history, name="stock-history"),
]
