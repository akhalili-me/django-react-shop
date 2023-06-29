from django.urls import path, include
from rest_framework import routers
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r"orders", OrderViewSet, basename="orders")
# router.register(r"orderitems", OrderItemViewSet, basename="order_item")

urlpatterns = [
    path("", CartItemsList.as_view()),
    path("create", CreateCartItems.as_view()),
    path("<int:pk>/", RDCartItems.as_view()),
    path("removeall", DeleteAllCartItems.as_view()),
    path("location", StateCityList.as_view()),
    path("orderitems",OrderItemCreate.as_view()),
    path("orderitems/<int:pk>/",RUDOrderItemView.as_view()),
    path("orderitemsbyorderid/<int:pk>/",OrderItemList.as_view()),
    path("", include(router.urls)),
]
