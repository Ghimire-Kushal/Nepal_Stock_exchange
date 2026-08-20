from django.urls import path
from .views import dashboard, system_statistics
urlpatterns=[path("dashboard/",dashboard), path("admin/statistics/", system_statistics)]
