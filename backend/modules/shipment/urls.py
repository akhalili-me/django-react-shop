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
        "address/<uuid:uuid>",
        AddressRetrieveUpdateDeleteView.as_view(),
        name="user-address-detail",
    ),
]
