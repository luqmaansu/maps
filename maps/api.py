from rest_framework.generics import ListAPIView
from .models import Location
from .serializers import LocationSerializer


class LocationListAPIView(ListAPIView):
    serializer_class = LocationSerializer

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
        # Return with info: Showing x of y locations
        x = len(self.get_queryset())
        y = Location.objects.count()
        response = super().list(request, *args, **kwargs)
        response["info"] = f"Showing {x} of {y} locations"
        return response
