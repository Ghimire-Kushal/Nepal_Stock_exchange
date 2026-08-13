from django.urls import path
from .views import WatchlistView, WatchDetail
urlpatterns=[path("",WatchlistView.as_view()),path("<int:pk>/",WatchDetail.as_view())]
