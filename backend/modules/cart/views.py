from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import DestroyAPIView, RetrieveUpdateDestroyAPIView
from modules.utility.permissions import IsSuperUserOrObjectOwner
from .serializers import (
    SessionAndCartItemsListSerializer,
    CartItemCreateSerializer,
    CartItemDetailsSerializer,
)
from .models import ShoppingSession, CartItem


class CartItemListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        shopping_session, _ = ShoppingSession.objects.get_or_create(user=request.user)
        serializer = SessionAndCartItemsListSerializer(shopping_session)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CartItemCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        shopping_session, _ = ShoppingSession.objects.get_or_create(user=request.user)
        serializer.save(session=shopping_session)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartItemReadUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsSuperUserOrObjectOwner]
    serializer_class = CartItemDetailsSerializer
    queryset = CartItem.objects.all()
    user_field = "session.user"
    lookup_field = "uuid"


class DeleteAllCartItems(DestroyAPIView):
    """
    Delete all cart items associated with the authenticated user.
    """

    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        shopping_session = get_object_or_404(ShoppingSession, user=request.user)
        shopping_session.clear_session()
        return Response(status=status.HTTP_204_NO_CONTENT)
