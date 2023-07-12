from rest_framework import serializers
from .models import *
from modules.products.serializers import ProductImageSerializer
from modules.products.models import Product

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


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["product", "quantity"]


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["amount", "status", "payment_method"]


class CreateOrderSerializer(serializers.ModelSerializer):
    payment_method = serializers.CharField(max_length=200)

    class Meta:
        model = Order
        fields = ["id", "address", "total", "shipping_price","payment_method"]


class ListOrderSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ["id", "status", "total", "created_at"]

    def get_status(self, obj):
        return obj.payment.status


class RUDOrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    payment = PaymentSerializer(read_only=True)
    full_address = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ["id", "full_address",
                  "address", "total", "payment", "order_items"]

    def get_full_address(self, obj):
        return str(obj.address)