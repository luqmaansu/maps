from django.contrib import admin
from .models import Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "latitude", "longitude")
    search_fields = (
        "name",
        "address",
        "latitude",
        "longitude",
        "opening_hours",
        "google_maps_url",
        "waze_url",
    )
