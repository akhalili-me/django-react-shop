from django.test import TestCase
from rest_framework.test import APIClient
from modules.products.models import Category, Product
from django.contrib.auth import get_user_model
from modules.shipment.models import Address
from modules.checkout.models import Payment
from modules.orders.models import Order, OrderItem
from modules.utility.tokens import generate_jwt_token
from django.urls import reverse
from unittest.mock import patch
from rest_framework import status
from ..serializers import (
    OrderDetailsSerializer,
    OrderItemSerializer,
    OrdersListSerializer,
)
from modules.discounts.models import Discount, DiscountUsage
from modules.notifications.tasks.order_email import send_order_confirm_email
from django.utils import timezone
from datetime import timedelta

ORDER_CREATE_LIST_URL = reverse("orders:order-create-list")


class OrderTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        parent_category = Category.objects.create(
            name="Test Parent",
            parent=None,
        )

        child_category = Category.objects.create(
            name="Test Child",
            parent=parent_category,
        )

        self.product = Product.objects.create(
            name="Test Product",
            category=child_category,
            description="Test product description",
            price=20.32,
            quantity=24,
        )

        # Set up order
        self.user = get_user_model().objects.create_user(
            username="testuser", email="test@gmail.com", password="testpass"
        )

        self.address = Address.objects.create(
            user=self.user,
            state="Test State",
            city="Test City",
            phone="09012342134",
            postal_code="1847382365",
            street_address="Test street address",
            house_number="434",
        )

        self.order = Order.objects.create(
            user=self.user,
            address=self.address,
            shipping_price=10,
            total=1000,
        )
        self.payment = Payment.objects.create(
            amount=1000, method="Test method", order=self.order
        )
        self.order_item = OrderItem.objects.create(
            order=self.order, product=self.product, quantity=1
        )

        self.discount = Discount.objects.create(
            name="test",
            value=20,
            type="fixed",
            expire_at=timezone.now() + timedelta(2),
            code="TEST",
        )

        tokens = generate_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
        self.ORDER_RUD_URL = reverse(
            "orders:order-retrieve-update-destroy", args=[self.order.pk]
        )

    # def test_order_create_api(self):
    #     payload = {
    #         "address": self.address.pk,
    #         "total": 24,
    #         "payment_method": "test method",
    #         "shipping_price": 10,
    #         "order_items": [{"product": self.product.pk, "quantity": 2}],
    #         "discount": self.discount.code,
    #     }

    #     with patch.object(send_order_confirm_email, "delay") as gi:
    #         gi.return_value = True
    #         response = self.client.post(ORDER_CREATE_LIST_URL, payload, format="json")
    #         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #         self.assertTrue(Order.objects.filter(pk=response.data["id"]).exists())
    #         self.assertTrue(
    #             Payment.objects.filter(pk=response.data["payment"]["id"]).exists()
    #         )
    #         self.assertEqual(len(response.data["order_items"]), 1)
    #         for order_item in response.data["order_items"]:
    #             self.assertTrue(OrderItem.objects.filter(pk=order_item["id"]).exists())
    #         self.assertTrue(
    #             DiscountUsage.objects.filter(
    #                 user=self.user,
    #                 discount_id=self.discount,
    #                 order_id=response.data["id"],
    #             ).exists()
    #         )

    def test_order_items_empty_exception(self):
        payload = {
            "address": self.address.pk,
            "total": 24,
            "method": "test method",
            "shipping_price": 10,
        }

        with patch.object(send_order_confirm_email, "delay") as gi:
            gi.return_value = True
            response = self.client.post(ORDER_CREATE_LIST_URL, payload, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_orders_list_api(self):
        response = self.client.get(ORDER_CREATE_LIST_URL, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = OrdersListSerializer([self.order], many=True).data
        self.assertEqual(response.data, expected_data)

    def test_retrieve_order_api(self):
        response = self.client.get(self.ORDER_RUD_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = OrderDetailsSerializer(self.order).data
        self.assertEqual(response.data, expected_data)

    def test_update_order_api(self):
        payload = {"shipping_price": 15, "total": 50}
        response = self.client.patch(self.ORDER_RUD_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_order = Order.objects.get(pk=self.order.pk)
        self.assertEqual(updated_order.shipping_price, 15)
        self.assertEqual(updated_order.total, 50)

    def test_delete_order_api(self):
        response = self.client.delete(self.ORDER_RUD_URL)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(pk=self.order.pk).exists())


class OrderItemTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        parent_category = Category.objects.create(
            name="Test Parent",
            parent=None,
        )

        child_category = Category.objects.create(
            name="Test Child",
            parent=parent_category,
        )

        self.product = Product.objects.create(
            name="Test Product",
            category=child_category,
            description="Test product description",
            price=20.32,
            quantity=24,
        )

        # Set up order
        self.user = get_user_model().objects.create_user(
            username="testuser", email="test@gmail.com", password="testpass"
        )

        self.address = Address.objects.create(
            user=self.user,
            state="Test State",
            city="Test City",
            phone="09012342134",
            postal_code="1847382365",
            street_address="Test street address",
            house_number="434",
        )
        self.order = Order.objects.create(
            user=self.user,
            address=self.address,
            shipping_price=10,
            total=1000,
        )

        self.payment = Payment.objects.create(
            amount=1000, method="Test method", order=self.order
        )

        self.order_item = OrderItem.objects.create(
            order=self.order, product=self.product, quantity=1
        )

        tokens = generate_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
        self.ORDER_ITEM_RUD_URL = reverse(
            "orders:order-item-retrieve-update-destroy", args=[self.order_item.pk]
        )

    def test_retrieve_order_item_api(self):
        response = self.client.get(self.ORDER_ITEM_RUD_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = OrderItemSerializer(self.order_item).data
        self.assertEqual(response.data, expected_data)

    def test_update_order_item_api(self):
        payload = {"quantity": 6}
        response = self.client.patch(self.ORDER_ITEM_RUD_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_order_item = OrderItem.objects.get(pk=self.order_item.pk)
        self.assertEqual(updated_order_item.quantity, 6)

    def test_delete_order_item_api(self):
        response = self.client.delete(self.ORDER_ITEM_RUD_URL)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(OrderItem.objects.filter(pk=self.order_item.pk).exists())
