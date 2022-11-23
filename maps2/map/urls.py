from django.conf.urls import url
from map.views import IndexView, PlaceCreateView, PlaceListView, PlaceResetView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^list/$', PlaceListView.as_view(), name="place-list"),
    url(r'^create/$', PlaceCreateView.as_view(), name="place-create"),
    url(r'^reset/$', PlaceResetView.as_view(), name="place-reset"),
]
