from rest_framework import serializers
from .models import CartItem, ShoppingSession
from modules.products.serializers import ProductSerializer


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


class CartItemDetailsSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta(CartItemCreateSerializer.Meta):
        pass


class SessionAndCartItemsListSerializer(serializers.ModelSerializer):
    cart_items = CartItemDetailsSerializer(many=True)

    class Meta:
        model = ShoppingSession
        fields = ["total", "cart_items"]
