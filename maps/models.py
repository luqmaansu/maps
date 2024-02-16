from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    latitude = models.CharField(max_length=10)
    longitude = models.CharField(max_length=10)
    opening_hours = models.JSONField()
    google_maps_url = models.URLField()
    waze_url = models.URLField()

    def __str__(self):
        return self.name
