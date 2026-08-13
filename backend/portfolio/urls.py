from django.urls import path
from .views import PortfolioList, PortfolioDetail, HoldingCreate, HoldingDetail, PortfolioSummary
urlpatterns = [path("", PortfolioList.as_view()), path("summary/", PortfolioSummary.as_view()), path("<int:pk>/", PortfolioDetail.as_view()), path("<int:portfolio_id>/holdings/", HoldingCreate.as_view()), path("holdings/<int:pk>/", HoldingDetail.as_view())]
