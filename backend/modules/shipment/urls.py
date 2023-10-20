from django.urls import path
from .views import (
    LocationListAPIView,
)

app_name = "shipment"

urlpatterns = [
    path("locations", LocationListAPIView.as_view(), name="locations-list"),
]
