from django.urls import path
from .views import (
    LocationListView,
    UserAddressListView,
    AddressRetrieveUpdateDeleteView,
)

app_name = "shipment"

urlpatterns = [
    path("locations", LocationListView.as_view(), name="locations-list"),
    path(
        "user-addresses", UserAddressListView.as_view(), name="user-address-create-list"
    ),
    path(
        "address/<int:pk>",
        AddressRetrieveUpdateDeleteView.as_view(),
        name="address-retrieve-update-delete",
    ),
]
