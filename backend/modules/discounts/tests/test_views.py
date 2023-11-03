from rest_framework.test import APIClient
from django.test import TestCase
from rest_framework import status
from modules.utility.tokens import generate_jwt_token
from django.urls import reverse
from ..models import Discount
from ..serializers import (
    DiscountSerializer,
)
from datetime import timedelta
from django.utils import timezone
from decimal import Decimal
from modules.utility.factories import (
    SuperUserFactory,
    DiscountFactory,
    ShoppingSessionFactory,
)

DISCOUNT_CREATE_URL = reverse("discounts:discount-create")
APPLY_DISCOUNT_URL = reverse("discounts:discount-apply")


class DiscountViewsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = SuperUserFactory()
        tokens = generate_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
        self.discount = DiscountFactory(value=20, user=None)
        self.DISCOUNT_RETRIEVE_UPDATE_DELETE_URL = reverse(
            "discounts:discount-retrieve-update-delete", args=[self.discount.pk]
        )

    def test_discount_create_view(self):
        payload = {
            "name": "test discount",
            "type": "percentage",
            "value": 25,
            "code": "SMMTCH",
            "expire_at": timezone.now() + timedelta(2),
        }
        response = self.client.post(DISCOUNT_CREATE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_discount_percentage_validation(self):
        payload = {
            "name": "test discount",
            "type": "percentage",
            "value": 125,
            "code": "SMMTCH",
            "expire_at": timezone.now() + timedelta(2),
        }
        response = self.client.post(DISCOUNT_CREATE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_discount_retrieve_view(self):
        response = self.client.get(self.DISCOUNT_RETRIEVE_UPDATE_DELETE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = DiscountSerializer(self.discount).data
        self.assertEqual(response.data, expected_data)

    def test_discount_update_view(self):
        payload = {
            "type": "fixed",
            "value": 43,
        }
        self.client.patch(self.DISCOUNT_RETRIEVE_UPDATE_DELETE_URL, payload)
        updated_discount = Discount.objects.get(pk=self.discount.pk)
        self.assertEqual(updated_discount.type, "fixed")
        self.assertEqual(updated_discount.value, 43)

    def test_discount_delete_view(self):
        response = self.client.delete(self.DISCOUNT_RETRIEVE_UPDATE_DELETE_URL)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Discount.objects.filter(pk=self.discount.pk).exists())

    def test_apply_discount_view(self):
        ShoppingSessionFactory(user=self.user, total=658)
        payload = {"code": self.discount.code}
        response = self.client.post(APPLY_DISCOUNT_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, Decimal("526.40"))
