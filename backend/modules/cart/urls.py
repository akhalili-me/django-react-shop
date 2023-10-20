from django.urls import path
from .views import (
    ListCreateUpdateCartItem,
    DestroyCartItem,
    DeleteAllCartItems,
)

app_name = "cart"

urlpatterns = [
    path("", ListCreateUpdateCartItem.as_view(), name="cart-items-list-create-update"),
    path("<int:product_id>", DestroyCartItem.as_view(), name="cart-item-delete"),
    path("removeall", DeleteAllCartItems.as_view(), name="delete-all-cart-items"),
]
