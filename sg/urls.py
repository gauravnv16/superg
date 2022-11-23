from django.urls import path

from .import views

urlpatterns = [
    path('sg',views.homepage,name="home")
]