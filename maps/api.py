from django.db.models import Q
from rest_framework.generics import ListAPIView
from django_filters import rest_framework as filters
from .models import Location
from .serializers import LocationSerializer


class LocationFilter(filters.FilterSet):

    general_search = filters.CharFilter(method="filter_general_search")

    class Meta:
        model = Location
        fields = ["name", "address", "latitude", "longitude"]

    def filter_general_search(self, queryset, name, value):
        # Search on multiple fields
        name_query = Q(name__icontains=value)
        address_query = Q(address__icontains=value)
        latitude_query = Q(latitude__icontains=value)
        longitude_query = Q(longitude__icontains=value)

        return queryset.filter(
            name_query | address_query | latitude_query | longitude_query
        )


class LocationListAPIView(ListAPIView):
    serializer_class = LocationSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = LocationFilter

    def get_queryset(self):
        # import time

        # time.sleep(1)
        return Location.objects.all()

    # Pass range to serializer as context
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["range"] = self.request.query_params.get("range", 0)
        return context

    def list(self, request, *args, **kwargs):
        filtered_queryset = self.filter_queryset(self.get_queryset())
        x = len(filtered_queryset)
        y = Location.objects.count()
        response = super().list(request, *args, **kwargs)
        response["info"] = f"Showing {x} of {y} locations"
        return response
