import json
from django.http.response import JsonResponse
from django.shortcuts import redirect
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from map.models import Place
from superg import settings


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context["API_KEY"] = settings.API_KEY
        context["TABLE_ID"] = settings.TABLE_ID
        return context


class PlaceCreateView(CreateView):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        try:
            latitude = data.get("latitude")
            longitude = data.get("longitude")
            address = data.get("address")
            place = Place.objects.create(latitude=latitude, longitude=longitude, address=address)
            context = {
                "object": {
                    "id": place.id,
                    "latitude": place.latitude,
                    "longitude": place.longitude,
                    "address": place.address
                },
                "result": True
            }
        except Exception :
            context = {
                "object": None,
                "result": False,
                "error": str(e)
            }
        return JsonResponse(context)


class PlaceListView(ListView):
    model = Place
    queryset = Place.objects.all()

    def get(self, request, *args, **kwargs):
        super(PlaceListView, self).get(request, *args, **kwargs)
        context = {"object_list": list(self.object_list.values("address", "latitude", "longitude"))}
        return JsonResponse(context)


class PlaceResetView(View):
    def get(self, request, *args, **kwargs):
        try:
            Place.objects.all().delete()
            result = True
        except Exception:
            result = False
        context = {"object_list": [], "result": result}
        return JsonResponse(context)
