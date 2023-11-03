from rest_framework import serializers
from .models import CartItem, ShoppingSession
from modules.products.serializers import ProductSerializer
from modules.utility.loading import get_model
from django.shortcuts import get_object_or_404

Product = get_model("products", "Product")


class CartItemCreateSerializer(serializers.ModelSerializer):
    product = serializers.SlugField()

    class Meta:
        model = CartItem
        fields = ["product"]

    def validate(self, data):
        self.product = get_object_or_404(Product, slug=data["product"])

        if self.product.quantity == 0:
            raise serializers.ValidationError("Out of stock")

        return data

    def create(self, validated_data):
        validated_data["product"] = self.product
        validated_data["quantity"] = 1
        return super().create(validated_data)


class CartItemDetailsSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta(CartItemCreateSerializer.Meta):
        fields = ["uuid", "product", "quantity"]

    def validate(self, data):
        product_quantity = self.instance.product.quantity
        if data["quantity"] > product_quantity:
            raise serializers.ValidationError("Can't add more products")

        return data


class SessionAndCartItemsListSerializer(serializers.ModelSerializer):
    cart_items = CartItemDetailsSerializer(many=True)

    class Meta:
        model = ShoppingSession
        fields = ["total", "cart_items"]
