from django.urls import path
from .views import FloorSheetList
urlpatterns = [path("", FloorSheetList.as_view())]
