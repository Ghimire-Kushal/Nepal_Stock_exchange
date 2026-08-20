from django.urls import path

from .views import StockDetailView, StockListView, stock_history, broker_analysis, technical_analysis, import_companies

urlpatterns = [
    path("", StockListView.as_view(), name="stock-list"),
    path("admin/import-companies/", import_companies, name="import-companies"),
    path("<str:symbol>/", StockDetailView.as_view(), name="stock-detail"),
    path("<str:symbol>/history/", stock_history, name="stock-history"),
    path("<str:symbol>/broker-analysis/", broker_analysis, name="broker-analysis"),
    path("<str:symbol>/technical-analysis/", technical_analysis, name="technical-analysis"),
]
