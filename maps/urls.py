from django.urls import path

from . import views
from . import api

urlpatterns = [
    path("", views.MapView.as_view(), name="map"),
    path("api/locations/", api.LocationListAPIView.as_view(), name="api-location-list"),
]
