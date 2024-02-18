from rest_framework import serializers
from .models import Location, Distance
from django.db.models import Subquery, Q


class LocationSerializer(serializers.ModelSerializer):
    nearby_locations = serializers.SerializerMethodField()
    has_nearby_locations = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = "__all__"

    def get_nearby_locations(self, obj):
        range_km = self.context.get("range")

        # Subquery to find origin IDs where obj is a destination
        origin_ids = Subquery(
            Distance.objects.filter(
                destination=obj,
                distance__lte=range_km,
            ).values_list("origin_id", flat=True)
        )

        # Subquery to find destination IDs where obj is an origin
        destination_ids = Subquery(
            Distance.objects.filter(
                origin=obj,
                distance__lte=range_km,
            ).values_list("destination_id", flat=True)
        )

        # Combine both subqueries to get unique location IDs
        location_ids = (
            Location.objects.filter(Q(id__in=origin_ids) | Q(id__in=destination_ids))
            .exclude(id=obj.id)
            .distinct()
        )

        # Serialize and return the nearby locations
        nearby_locations = location_ids.values_list("name", flat=True)
        return list(nearby_locations)

    def get_has_nearby_locations(self, obj):
        range_km = self.context.get("range")

        # Check if there is any Distance object meeting the condition
        distances = Distance.objects.filter(
            Q(origin=obj, distance__lte=range_km)
            | Q(destination=obj, distance__lte=range_km)
        ).exclude(pk=obj.pk)

        condition = distances.exists()

        return condition
