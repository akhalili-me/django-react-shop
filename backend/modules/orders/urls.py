from django.urls import path
from .views import (
    OrderRetrieveUpdateDestroyView,
    OrderItemRetrieveUpdateDestroyView,
    ListCreateOrderView,
)

app_name = "orders"

urlpatterns = [
    path("", ListCreateOrderView.as_view(), name="create-list"),
    path(
        "<uuid:uuid>",
        OrderRetrieveUpdateDestroyView.as_view(),
        name="detail",
    ),
    path(
        "items/<uuid:uuid>",
        OrderItemRetrieveUpdateDestroyView.as_view(),
        name="order-item-detail",
    ),
]
