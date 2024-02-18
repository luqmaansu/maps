from django.core.management.base import BaseCommand
from maps.models import Location, Distance
import math
from django.db import transaction


class Command(BaseCommand):
    help = "Populates distances between locations"

    def handle(self, *args, **kwargs):
        self.populate_distances()

    def haversine(self, coord1, coord2):
        lat1, lon1 = coord1  # Correctly unpack the first coordinate tuple
        lat2, lon2 = coord2  # Correctly unpack the second coordinate tuple

        # convert to float
        lat1 = float(lat1)
        lon1 = float(lon1)
        lat2 = float(lat2)
        lon2 = float(lon2)

        R = 6371  # Earth radius in kilometers

        dLat = math.radians(lat2 - lat1)
        dLon = math.radians(lon2 - lon1)
        lat1 = math.radians(lat1)
        lat2 = math.radians(lat2)

        a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.cos(lat1) * math.cos(
            lat2
        ) * math.sin(dLon / 2) * math.sin(dLon / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = R * c
        return distance

    def populate_distances(self):
        locations = list(Location.objects.all())
        distance_objects = []  # List to hold Distance objects before bulk creation
        total_locations = len(locations)
        distance_count = 0

        with transaction.atomic():  # Use a transaction to wrap the bulk create
            for i in range(total_locations):
                loc1 = locations[i]

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Processing location {i+1} of {total_locations}: {loc1.name}"
                    )
                )

                for j in range(i + 1, total_locations):
                    loc2 = locations[j]
                    distance = self.haversine(
                        (loc1.latitude, loc1.longitude), (loc2.latitude, loc2.longitude)
                    )
                    distance = round(distance, 4)
                    distance_objects.append(
                        Distance(origin=loc1, destination=loc2, distance=distance)
                    )
                    distance_count += 1

                # Bulk create after processing each location to manage memory usage
                if distance_objects:
                    Distance.objects.bulk_create(distance_objects)
                    distance_objects.clear()

        self.stdout.write(
            self.style.SUCCESS(f"Successfully populated {distance_count} distances")
        )
