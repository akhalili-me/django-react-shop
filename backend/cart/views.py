from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import ShoppingSession
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics
from .permissions import isCartOwner
from products.models import Product
from django.http import Http404

class CreateCartItems(generics.CreateAPIView):
    """
    View for creating cart items.
    """
    serializer_class = CartItemCreateSerializer
    permission_classes = [IsAuthenticated]

    def update_shopping_session(self,shopping_session):
        shopping_session.total = shopping_session.calculate_total()
        shopping_session.save()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']
        shopping_session, _ = ShoppingSession.objects.get_or_create(user=self.request.user)

        CartItem.objects.update_or_create(
            product=product,
            session=shopping_session,
            defaults={'quantity': quantity}
        )

        self.update_shopping_session(shopping_session)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,status=status.HTTP_201_CREATED,headers=headers)

class RDCartItems(generics.RetrieveDestroyAPIView):
    """
    View for retrieve and delete cart items.
    """
    serializer_class = RDCartItemSerializer
    permission_classes = [IsAuthenticated,isCartOwner]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_cart_item_by_product_id(kwargs.get('pk'))
        serilizer = self.serializer_class(instance=instance)
        return Response(serilizer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_cart_item_by_product_id(kwargs.get('pk'))
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get_cart_item_by_product_id(self, id):
        cart_item = CartItem.objects.get(product__id=id,session__user=self.request.user)
        return cart_item

    
class CartItemsList(generics.ListAPIView):
    """
    Get session and cart items associated with it.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemsListSerializer

    def get_queryset(self):
        session = ShoppingSession.objects.filter(user=self.request.user)
        return session
    
