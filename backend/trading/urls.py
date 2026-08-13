from django.urls import path
from .views import TradeView, TradingSummary
urlpatterns=[path("",TradeView.as_view()),path("summary/",TradingSummary.as_view())]
