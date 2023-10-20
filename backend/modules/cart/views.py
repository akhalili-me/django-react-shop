from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import (
    DestroyAPIView,
)
from modules.utility.permissions import IsSuperUserOrObjectOwner
from .serializers import (
    SessionAndCartItemsListSerializer,
    CartItemCreateSerializer,
)
from .models import ShoppingSession, CartItem


class ListCreateUpdateCartItem(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        shopping_session, _ = ShoppingSession.objects.get_or_create(user=request.user)
        serializer = SessionAndCartItemsListSerializer(shopping_session)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CartItemCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        shopping_session, _ = ShoppingSession.objects.get_or_create(user=request.user)
        CartItem.objects.update_or_create(
            product=serializer.validated_data["product"],
            session=shopping_session,
            defaults={"quantity": serializer.validated_data["quantity"]},
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DestroyCartItem(DestroyAPIView):
    permission_classes = [IsSuperUserOrObjectOwner]
    queryset = CartItem.objects.all()
    user_field = "session.user"
    lookup_field = "product__id"
    lookup_url_kwarg = "product_id"


class DeleteAllCartItems(DestroyAPIView):
    """
    Delete all cart items associated with the authenticated user.
    """

    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        shopping_session = get_object_or_404(ShoppingSession, user=request.user)
        CartItem.objects.filter(session=shopping_session).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
