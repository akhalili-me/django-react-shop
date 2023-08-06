from django.urls import path
from .views import (
    CreateCartItems,
    CartItemsList,
    RUDCartItem,
    DeleteAllCartItems,
    StateCityList,
    RUDOrderItemView,
    RUDPaymentView,
    CreateOrdersView,
    ListUserOrdersView,
    RUDOrderView,
)

urlpatterns = [
    path("", CartItemsList.as_view(), name="cart-items-list"),
    path("create", CreateCartItems.as_view(), name="create-cart-items"),
    path("<int:pk>", RUDCartItem.as_view(), name="retrieve-update-delete-cart-item"),
    path("removeall", DeleteAllCartItems.as_view(), name="delete-all-cart-items"),
    path("location", StateCityList.as_view(), name="state-city-list"),
    path("orderitems/<int:pk>", RUDOrderItemView.as_view(), name="rud-order-item"),
    path("payment/<int:pk>", RUDPaymentView.as_view(), name="rud-payment"),
    path("orders/create", CreateOrdersView.as_view(), name="create-order"),
    path("orders/", ListUserOrdersView.as_view(), name="list-user-order"),
    path("orders/<int:pk>", RUDOrderView.as_view(), name="rud-order"),
]
