from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import ShoppingSession
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics
from .permissions import isCartOwner

class CreateCartItems(generics.CreateAPIView):
    """
    View for creating cart items.
    """
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def save_and_update_shopping_session(self,cart_item):
        shopping_session, _ = ShoppingSession.objects.get_or_create(user=self.request.user)
        with transaction.atomic():
            cart_item.session = shopping_session
            cart_item.save()
            shopping_session.total = shopping_session.calculate_total()
            shopping_session.save()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart_item = serializer.save()
        self.save_and_update_shopping_session(cart_item)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,status=status.HTTP_201_CREATED,headers=headers)

class RUDCartItems(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieve, update and delete cart items.
    """
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated,isCartOwner]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_cart_item(kwargs.get('pk'))
        serilizer = self.serializer_class(instance=instance)
        return Response(serilizer.data)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_cart_item(kwargs.get('pk'))
        serializer = self.serializer_class(instance=instance, data=request.data)
        self.perform_update(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_cart_item(kwargs.get('pk'))
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get_cart_item(self,id):
        cart_item = get_object_or_404(CartItem,id=id)
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
    
