from rest_framework.viewsets import ModelViewSet
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    UserCommentsSerializer,
    CommentSerializer,
    AddressSerializer,
    UserSerializer,
)
from modules.products.models import Comment
from modules.cart.models import Address
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from .pagination import UserCommentListPagination


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserRegisterView(generics.CreateAPIView):
    """
    Viewset for creating user.
    """

    serializer_class = UserSerializer


class UserCommentsListView(generics.ListAPIView):
    """
    Return the comments along with product associated with the authenticated user.
    """

    serializer_class = UserCommentsSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = UserCommentListPagination

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user).order_by("-created_at")


class RUDCommentsView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieve, update and destroy comments.
    """

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(
            id=self.kwargs.get("pk"), author=self.request.user
        )


class AddressViewSet(ModelViewSet):
    """
    View set for retrieve, update, delete and create address.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
