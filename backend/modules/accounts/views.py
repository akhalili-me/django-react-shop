from rest_framework import generics
from .serializers import (
    UserSerializer,
)
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserRegisterView(generics.CreateAPIView):
    """
    Viewset for creating user.
    """

    serializer_class = UserSerializer
