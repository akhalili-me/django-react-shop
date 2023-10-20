from django.urls import path
from .views import (
    OrderRetrieveUpdateDestroyView,
    OrderItemRetrieveUpdateDestroyView,
    ListCreateOrderView,
)

app_name = "orders"

urlpatterns = [
    path("", ListCreateOrderView.as_view(), name="order-create-list"),
    path(
        "orders/<int:pk>",
        OrderRetrieveUpdateDestroyView.as_view(),
        name="order-retrieve-update-destroy",
    ),
    path(
        "items/<int:pk>",
        OrderItemRetrieveUpdateDestroyView.as_view(),
        name="order-item-retrieve-update-destroy",
    ),
]
