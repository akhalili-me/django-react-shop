from django.urls import path
from .views import (
    ListCreateUpdateCartItem,
    DestroyCartItem,
    DeleteAllCartItems,
    StateCityList,
    OrderRetrieveUpdateDestroyView,
    OrderItemRetrieveUpdateDestroyView,
    PaymentRetrieveUpdateDestroyView,
    ListCreateOrderView,
)

app_name = "cart"

urlpatterns = [
    path("", ListCreateUpdateCartItem.as_view(), name="cart-items-list-create-update"),
    path("<int:product_id>", DestroyCartItem.as_view(), name="cart-item-delete"),
    path("removeall", DeleteAllCartItems.as_view(), name="delete-all-cart-items"),
    path("location", StateCityList.as_view(), name="state-city-list"),
    path(
        "orderitems/<int:pk>",
        OrderItemRetrieveUpdateDestroyView.as_view(),
        name="order-item-retrieve-update-destroy",
    ),
    path(
        "payment/<int:order_id>",
        PaymentRetrieveUpdateDestroyView.as_view(),
        name="payment-retrieve-update-destroy",
    ),
    path("orders/", ListCreateOrderView.as_view(), name="order-create-list"),
    path(
        "orders/<int:pk>",
        OrderRetrieveUpdateDestroyView.as_view(),
        name="order-retrieve-update-destroy",
    ),
]
