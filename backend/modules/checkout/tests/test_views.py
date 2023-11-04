from rest_framework.test import APIClient
from django.test import TestCase
from rest_framework import status
from ..models import Payment
from ..serializers import (
    PaymentSerializer,
)
from modules.utility.tokens import apply_jwt_token_credentials_to_client
from modules.utility.factories import UserFactory, PaymentFactory, OrderFactory


class PaymentTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.order = OrderFactory(user=self.user)
        self.payment = PaymentFactory(order=self.order)
        apply_jwt_token_credentials_to_client(self.client, self.user)

    def test_retrieve_payment_api(self):
        response = self.client.get(self.payment.get_absolute_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = PaymentSerializer(self.payment).data
        self.assertEqual(response.data, expected_data)

    def test_update_payment_api(self):
        payload = {"status": "paid", "method": "updated_method"}
        response = self.client.patch(self.payment.get_absolute_url(), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_payment = Payment.objects.get(pk=self.payment.pk)
        self.assertEqual(updated_payment.status, "paid")
        self.assertEqual(updated_payment.method, "updated_method")

    def test_delete_payment_api(self):
        response = self.client.delete(self.payment.get_absolute_url())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Payment.objects.filter(pk=self.payment.pk).exists())
