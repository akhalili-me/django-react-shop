from rest_framework import serializers
from .models import *

class CartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ['product','quantity']

class CartItemsListSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = ShoppingSession
        fields = ['total', 'cart_items']