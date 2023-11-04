from django.test import TestCase
from rest_framework.test import APIClient
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
from modules.discounts.models import DiscountUsage
from modules.notifications.tasks.order_email import send_order_confirm_email
from modules.utility.factories import (
    UserFactory,
    OrderFactory,
    OrderItemFactory,
    DiscountFactory,
    UserAddressFactory,
)

ORDER_CREATE_LIST_URL = reverse("orders:create-list")


class OrderTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.user_address = UserAddressFactory(user=self.user)
        self.order = OrderFactory(user=self.user)
        self.order_item = OrderItemFactory(order=self.order)
        self.product = self.order_item.product
        self.discount = DiscountFactory(user=None)
        tokens = generate_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')

    def test_order_create_api(self):
        payload = {
            "address": self.user_address.uuid,
            "total": 24,
            "payment_method": "test method",
            "shipping_price": 10,
            "order_items": [{"product": self.product.pk, "quantity": 2}],
            "discount": self.discount.code,
        }

        with patch.object(send_order_confirm_email, "delay") as gi:
            gi.return_value = True
            response = self.client.post(ORDER_CREATE_LIST_URL, payload, format="json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertTrue(Order.objects.filter(pk=response.data["id"]).exists())
            self.assertTrue(
                Payment.objects.filter(uuid=response.data["payments"][0]["uuid"]).exists()
            )
            self.assertEqual(len(response.data["order_items"]), 1)
            for order_item in response.data["order_items"]:
                self.assertTrue(OrderItem.objects.filter(pk=order_item["id"]).exists())
            self.assertTrue(
                DiscountUsage.objects.filter(
                    user=self.user,
                    discount_id=self.discount,
                    order_id=response.data["id"],
                ).exists()
            )

    def test_order_items_empty_exception(self):
        payload = {
            "address": self.user_address.uuid,
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
        response = self.client.get(self.order.get_absolute_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = OrderDetailsSerializer(self.order).data
        self.assertEqual(response.data, expected_data)

    def test_update_order_api(self):
        payload = {"shipping_price": 15, "total": 50}
        response = self.client.patch(self.order.get_absolute_url(), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_order = Order.objects.get(pk=self.order.pk)
        self.assertEqual(updated_order.shipping_price, 15)
        self.assertEqual(updated_order.total, 50)

    def test_delete_order_api(self):
        response = self.client.delete(self.order.get_absolute_url())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(pk=self.order.pk).exists())


class OrderItemTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.order = OrderFactory(user=self.user)
        self.order_item = OrderItemFactory(order=self.order)
        tokens = generate_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')

    def test_retrieve_order_item_api(self):
        response = self.client.get(self.order_item.get_absolute_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = OrderItemSerializer(self.order_item).data
        self.assertEqual(response.data, expected_data)

    def test_update_order_item_api(self):
        payload = {"quantity": 6}
        response = self.client.patch(self.order_item.get_absolute_url(), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_order_item = OrderItem.objects.get(pk=self.order_item.pk)
        self.assertEqual(updated_order_item.quantity, 6)

    def test_delete_order_item_api(self):
        response = self.client.delete(self.order_item.get_absolute_url())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(OrderItem.objects.filter(pk=self.order_item.pk).exists())
