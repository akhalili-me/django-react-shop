from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r"orders", OrderViewSet, basename="orders")

urlpatterns = [
    path("", CartItemsList.as_view(), name="cart-items-list"),
    path("create/", CreateCartItems.as_view(), name="create-cart-items"),
    path("<int:pk>/", RDCartItems.as_view(), name="retrieve-delete-cart-items"),
    path("removeall/", DeleteAllCartItems.as_view(), name="delete-all-cart-items"),
    path("location/", StateCityList.as_view(), name="state-city-list"),
    path("orderitems/<int:pk>/", RUDOrderItemView.as_view(), name="rud-order-item"),
    path("payment/<int:pk>/", RUDPaymentView.as_view(), name="rud-payment"),
    path("", include(router.urls)),
]
