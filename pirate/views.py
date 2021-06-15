from django.shortcuts import render

from django.views import generic
from .models import Pirate
# Create your views here.

class IndexView(generic.ListView):
    template_name = "pirate/index.html"
    context_object_name = "pirate_list"

    def get_queryset(self):
        """Return the all pirates."""
        return Pirate.objects.order_by("name")

class DetailView(generic.DetailView):
    model = Pirate
    template_name = "pirate/detail.html"
