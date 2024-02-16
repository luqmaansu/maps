from django.views.generic import ListView
from .models import Location


class MapView(ListView):
    model = Location
    template_name = "maps/map.html"
