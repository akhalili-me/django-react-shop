from django.urls import path
from .views import (
    CartItemListCreateView,
    CartItemReadUpdateDeleteView,
    DeleteAllCartItems,
)

app_name = "cart"

urlpatterns = [
    path("", CartItemListCreateView.as_view(), name="cart-items-list-create"),
    path(
        "<uuid:uuid>", CartItemReadUpdateDeleteView.as_view(), name="cart-item-detail"
    ),
    path("removeall", DeleteAllCartItems.as_view(), name="delete-all-cart-items"),
]
