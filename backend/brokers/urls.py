from django.urls import path
from .views import BrokerList, BrokerDetail, broker_activity
urlpatterns = [path("", BrokerList.as_view()), path("<int:broker_number>/", BrokerDetail.as_view()), path("<int:broker_number>/activity/", broker_activity)]
