from rest_framework import serializers
from .models import OrderItem, Order
from modules.products.serializers import ProductImageSerializer
from modules.products.models import Product
from modules.checkout.serializers import PaymentSerializer

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
    order_items = OrderItemSerializer(many=True,required=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "address",
            "total",
            "shipping_price",
            "payment_method",
            "order_items",
        ]



class OrdersListSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ["id", "status", "total", "created_at"]

    def get_status(self, obj):
        return obj.payment.status


class OrderItemsSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "quantity", "product"]


class OrderDetailsSerializer(serializers.ModelSerializer):
    order_items = OrderItemsSerializer(many=True, read_only=True)
    payment = PaymentSerializer(read_only=True)
    full_address = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "full_address",
            "address",
            "total",
            "payment",
            "order_items",
            "shipping_price",
            "created_at",
        ]

    def get_full_address(self, obj):
        return str(obj.address)
