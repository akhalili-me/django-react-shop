from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from .views import (
    UserRegisterView,
    CustomTokenObtainPairView,
)

app_name = "accounts"

urlpatterns = [
    path("register", UserRegisterView.as_view(), name="register"),
    path("token", CustomTokenObtainPairView.as_view(), name="token_obtain"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),

]
