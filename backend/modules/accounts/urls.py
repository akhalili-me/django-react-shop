from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from .views import (
    UserRegisterView,
    CustomTokenObtainPairView,
    UserCommentsListView,
    RUDCommentsView,
    AddressViewSet,
)

from rest_framework import routers

router = routers.DefaultRouter()

router.register(r"address", AddressViewSet, basename="address")

urlpatterns = [
    path("", include(router.urls)),
    path("register", UserRegisterView.as_view(), name="user_register"),
    path("token", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("comments/", UserCommentsListView.as_view(), name="user_comments"),
    path("comments/<int:pk>", RUDCommentsView.as_view(), name="user_comments_RUD"),
]
