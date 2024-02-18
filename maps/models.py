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


class Distance(models.Model):
    origin = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="origin"
    )
    destination = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="destination"
    )
    distance = models.FloatField(help_text="Distance in km")

    def __str__(self):
        return f"{self.origin} - {self.destination}"

    # Unique together origin and destination
    class Meta:
        unique_together = ("origin", "destination")
