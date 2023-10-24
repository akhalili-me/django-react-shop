from rest_framework.test import APIClient
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from modules.products.models import Category, Product
from modules.utility.images import create_test_image
from modules.utility.tokens import generate_jwt_token
from django.urls import reverse
from ..models import Payment
from ..serializers import (
    PaymentSerializer,
)
from modules.shipment.models import Address
from modules.orders.models import Order


class PaymentTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        parent_category = Category.objects.create(
            name="Test Parent",
            parent=None,
            image=create_test_image(),
        )

        child_category = Category.objects.create(
            name="Test Child",
            parent=parent_category,
            image=create_test_image(),
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
        tokens = generate_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
        self.PAYMENT_RETRIEVE_UPDATE_DELETE_URL = reverse(
            "checkout:payment-retrieve-update-destroy", args=[self.order.pk]
        )

    def test_retrieve_payment_api(self):
        response = self.client.get(self.PAYMENT_RETRIEVE_UPDATE_DELETE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = PaymentSerializer(self.payment).data
        self.assertEqual(response.data, expected_data)

    def test_update_payment_api(self):
        payload = {"status": "paid", "method": "updated_method"}
        response = self.client.patch(self.PAYMENT_RETRIEVE_UPDATE_DELETE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_payment = Payment.objects.get(pk=self.payment.pk)
        self.assertEqual(updated_payment.status, "paid")
        self.assertEqual(updated_payment.method, "updated_method")

    def test_delete_payment_api(self):
        response = self.client.delete(self.PAYMENT_RETRIEVE_UPDATE_DELETE_URL)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Payment.objects.filter(pk=self.payment.pk).exists())
