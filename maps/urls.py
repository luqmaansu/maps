from django.urls import path

from .api import LocationListAPIView

urlpatterns = [
    path("api/locations/", LocationListAPIView.as_view(), name="api-location-list")
]
