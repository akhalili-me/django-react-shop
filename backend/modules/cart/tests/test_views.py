from rest_framework.test import APIClient
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from modules.products.models import Category, Product
from modules.utility.images import create_test_image
from modules.utility.tokens import generate_jwt_token
from django.urls import reverse
from unittest.mock import patch
from ..tasks.order_email import send_order_confirm_email
from ..models import (
    CartItem,
    ShoppingSession,
    State,
    City,
    Address,
    Order,
    OrderItem,
    Payment,
)
from ..serializers import (
    RDCartItemSerializer,
    CartItemsListSerializer,
    StateCityListSerilizer,
    ListOrderSerializer,
    RUDOrderSerializer,
    PaymentSerializer,
    OrderItemSerializer,
)

CART_ITEM_CREATE_URL = reverse("cart:create-cart-item")
CART_ITEM_LIST_URL = reverse("cart:cart-items-list")
CART_ITEM_DELETE_ALL_URL = reverse("cart:delete-all-cart-items")
STATE_CITY_LIST_URL = reverse("cart:state-city-list")
ORDER_CREATE_URL = reverse("cart:create-order")
USER_ORDERS_LIST_URL = reverse("cart:list-user-order")


class CartItemCreateViewTests(TestCase):
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
        self.user = get_user_model().objects.create_user(
            username="testuser", email="test@gmail.com", password="testpass"
        )
        tokens = generate_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')

    def test_cart_item_create_api(self):
        payload = {"product": self.product.pk, "quantity": 2}
        response = self.client.post(CART_ITEM_CREATE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CartItem.objects.count(), 1)
        user_shopping_session = ShoppingSession.objects.get(user=self.user)
        self.assertTrue(
            CartItem.objects.filter(
                session=user_shopping_session, product=self.product
            ).exists()
        )


class CartItemRDTests(TestCase):
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
        self.user = get_user_model().objects.create_user(
            username="testuser", email="test@gmail.com", password="testpass"
        )
        self.shopping_session = ShoppingSession.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(
            product=self.product, quantity=1, session=self.shopping_session
        )
        tokens = generate_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
        self.CART_ITEM_RD_URL = reverse("cart:RD-cart-item", args=[self.product.pk])

    def test_retrieve_cart_item_api(self):
        response = self.client.get(self.CART_ITEM_RD_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = RDCartItemSerializer(self.cart_item).data
        self.assertEqual(response.data, expected_data)

    def test_delete_cart_item_api(self):
        response = self.client.delete(self.CART_ITEM_RD_URL)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CartItem.objects.filter(pk=self.cart_item.pk).exists())

    def test_cart_item_list_api(self):
        response = self.client.get(CART_ITEM_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = CartItemsListSerializer(self.shopping_session).data
        self.assertEqual(response.data, expected_data)

    def test_cart_item_delete_all_api(self):
        response = self.client.delete(CART_ITEM_DELETE_ALL_URL)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            self.assertFalse(
                CartItem.objects.filter(session=self.shopping_session).exists()
            )
        )


class StateCityTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.state = State.objects.create(name="Test state")
        self.city = City.objects.create(name="Test city", state=self.state)

    def test_state_city_list_api(self):
        response = self.client.get(STATE_CITY_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = StateCityListSerilizer([self.state], many=True).data
        self.assertEqual(response.data, expected_data)


class OrderTests(TestCase):
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

        self.payment = Payment.objects.create(
            amount=1000,
            payment_method="Test method",
        )

        self.order = Order.objects.create(
            user=self.user,
            address=self.address,
            payment=self.payment,
            shipping_price=10,
            total=1000,
        )

        self.order_item = OrderItem.objects.create(
            order=self.order, product=self.product, quantity=1
        )

        tokens = generate_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
        self.ORDER_RUD_URL = reverse("cart:rud-order", args=[self.order.pk])

    def test_order_create_api(self):
        payload = {
            "address": self.address.pk,
            "total": 24,
            "payment": {"payment_method": "test method"},
            "shipping_price": 10,
            "order_items": [{"product": self.product.pk, "quantity": 2}],
        }
        with patch.object(send_order_confirm_email,'delay') as gi:
            gi.return_value = True
            response = self.client.post(ORDER_CREATE_URL, payload, format="json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertTrue(Order.objects.filter(pk=response.data["id"]).exists())
            self.assertTrue(
                Payment.objects.filter(pk=response.data["payment"]["id"]).exists()
            )
            self.assertEqual(len(response.data["order_items"]), 1)
            for order_item in response.data["order_items"]:
                self.assertTrue(OrderItem.objects.filter(pk=order_item["id"]).exists())

    def test_user_orders_list_api(self):
        response = self.client.get(USER_ORDERS_LIST_URL, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = ListOrderSerializer([self.order], many=True).data
        self.assertEqual(response.data, expected_data)

    def test_retrieve_order_api(self):
        response = self.client.get(self.ORDER_RUD_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = RUDOrderSerializer(self.order).data
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

        self.payment = Payment.objects.create(
            amount=1000,
            payment_method="Test method",
        )

        self.order = Order.objects.create(
            user=self.user,
            address=self.address,
            payment=self.payment,
            shipping_price=10,
            total=1000,
        )

        tokens = generate_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
        self.PAYMENT_RUD_URL = reverse("cart:rud-payment", args=[self.order.pk])

    def test_retrieve_payment_api(self):
        response = self.client.get(self.PAYMENT_RUD_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = PaymentSerializer(self.payment).data
        self.assertEqual(response.data, expected_data)

    def test_update_payment_api(self):
        payload = {"status": "paid", "payment_method": "updated_method"}
        response = self.client.patch(self.PAYMENT_RUD_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_payment = Payment.objects.get(pk=self.payment.pk)
        self.assertEqual(updated_payment.status, "paid")
        self.assertEqual(updated_payment.payment_method, "updated_method")

    def test_delete_payment_api(self):
        response = self.client.delete(self.PAYMENT_RUD_URL)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Payment.objects.filter(pk=self.payment.pk).exists())


class OrderItemTests(TestCase):
    def setUp(self) -> None:
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

        self.payment = Payment.objects.create(
            amount=1000,
            payment_method="Test method",
        )

        self.order = Order.objects.create(
            user=self.user,
            address=self.address,
            payment=self.payment,
            shipping_price=10,
            total=1000,
        )

        self.order_item = OrderItem.objects.create(
            order=self.order, product=self.product, quantity=1
        )

        tokens = generate_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
        self.ORDER_ITEM_RUD_URL = reverse(
            "cart:rud-order-item", args=[self.order_item.pk]
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
