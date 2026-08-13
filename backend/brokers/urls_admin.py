from django.urls import path
from .views import import_floorsheet
urlpatterns = [path("import/", import_floorsheet)]
