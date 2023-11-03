from rest_framework.test import APIClient
from django.test import TestCase
from rest_framework import status
from modules.utility.tokens import generate_jwt_token
from django.urls import reverse
from ..models import (
    CartItem,
    ShoppingSession,
)
from ..serializers import (
    SessionAndCartItemsListSerializer,
)
from modules.utility.factories import ProductFactory, UserFactory, CartItemFactory

CART_ITEM_CREATE_LIST_UPDATE_URL = reverse("cart:cart-items-list-create-update")
CART_ITEM_DELETE_ALL_URL = reverse("cart:delete-all-cart-items")


class CartItemCreateViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.product = ProductFactory()
        self.user = UserFactory()
        tokens = generate_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')

    def test_cart_item_create_api(self):
        payload = {"product": self.product.pk, "quantity": 2}
        response = self.client.post(CART_ITEM_CREATE_LIST_UPDATE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CartItem.objects.count(), 1)
        user_shopping_session = ShoppingSession.objects.get(user=self.user)
        self.assertTrue(
            CartItem.objects.filter(
                session=user_shopping_session, product=self.product
            ).exists()
        )


class CartItemDestroyTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.cart_item = CartItemFactory()
        self.product = self.cart_item.product
        self.shopping_session = self.cart_item.session
        self.user = self.cart_item.session.user
        tokens = generate_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
        self.CART_ITEM_DELETE_URL = reverse(
            "cart:cart-item-delete", args=[self.product.pk]
        )

    def test_delete_cart_item_api(self):
        response = self.client.delete(self.CART_ITEM_DELETE_URL)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CartItem.objects.filter(pk=self.cart_item.pk).exists())

    def test_cart_item_list_api(self):
        response = self.client.get(CART_ITEM_CREATE_LIST_UPDATE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = SessionAndCartItemsListSerializer(self.shopping_session).data
        self.assertEqual(response.data, expected_data)

    def test_cart_item_delete_all_api(self):
        response = self.client.delete(CART_ITEM_DELETE_ALL_URL)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            self.assertFalse(
                CartItem.objects.filter(session=self.shopping_session).exists()
            )
        )
