from rest_framework import serializers
from .models import OrderItem, Order
from modules.products.serializers import ProductImageSerializer
from modules.products.models import Product
from modules.checkout.serializers import PaymentSerializer
from modules.discounts.services import DiscountService
from django.shortcuts import get_object_or_404
from modules.utility.loading import get_model

UserAddress = get_model("shipment", "UserAddress")


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "price", "quantity", "images"]


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["product", "quantity"]


class OrderCreateSerializer(serializers.ModelSerializer):
    payment_method = serializers.CharField(max_length=200)
    order_items = OrderItemSerializer(many=True, required=True)
    discount = serializers.CharField(allow_null=True, required=False)
    address = serializers.UUIDField()

    class Meta:
        model = Order
        fields = [
            "id",
            "address",
            "total",
            "shipping_price",
            "payment_method",
            "order_items",
            "discount",
        ]

    def validate_discount(self, value):
        user = self.context["request"].user
        DiscountService.validate_discount(value, user)
        return value

    def validate_address(self, value):
        get_object_or_404(UserAddress, uuid=value)
        return value


class OrdersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "status", "total", "created_at"]


class OrderItemsSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "quantity", "product"]


class OrderDetailsSerializer(serializers.ModelSerializer):
    order_items = OrderItemsSerializer(many=True, read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)
    full_address = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "full_address",
            "total",
            "payments",
            "order_items",
            "shipping_price",
            "created_at",
        ]

    def get_full_address(self, obj):
        return str(obj.billing_address)
