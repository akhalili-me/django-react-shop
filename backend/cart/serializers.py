from rest_framework import serializers
from .models import *
from products.serializers import ProductImageSerializer
from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "price", "quantity", "images"]


class CartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["product", "quantity"]

    def validate(self, data):
        product_quantity = data["product"].quantity
        cart_item_quantity = data["quantity"]

        if product_quantity < cart_item_quantity:
            raise serializers.ValidationError(
                "Product quantity is less than cart item quantity"
            )

        return data


class RDCartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ["product", "quantity"]

    def validate(self, data):
        product_quantity = data["product"].quantity
        cart_item_quantity = data["quantity"]

        if product_quantity < cart_item_quantity:
            raise serializers.ValidationError(
                "Product quantity is less than cart item quantity"
            )

        return data


class CartItemsListSerializer(serializers.ModelSerializer):
    cart_items = RDCartItemSerializer(many=True, read_only=True)

    class Meta:
        model = ShoppingSession
        fields = ["total", "cart_items"]


class StateCityListSerilizer(serializers.ModelSerializer):
    cities = serializers.StringRelatedField(many=True)

    class Meta:
        model = State
        fields = ["name", "cities"]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["address", "status", "total"]


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["order", "product", "quantity"]
