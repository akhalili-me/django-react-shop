from django.test import TestCase
from ..models import (
    ShoppingSession,
    CartItem,
)
from django.contrib.auth import get_user_model
from modules.products.models import Product, Category
from decimal import Decimal
from modules.utility.images import create_test_image


class ShoppingSessionTestCase(TestCase):
    def setUp(self):
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

    def test_shopping_session_creation(self):
        self.assertEqual(ShoppingSession.objects.count(), 1)
        self.assertEqual(self.shopping_session.user, self.user)
        self.assertEqual(self.shopping_session.total, 0)

    def test_update_total_method(self):
        CartItem.objects.create(
            session=self.shopping_session, product=self.product, quantity=2
        )
        self.assertEqual(
            self.shopping_session.total,
            Decimal(self.product.price * 2).quantize(Decimal("0.00")),
        )

    def test_shopping_session_update(self):
        self.shopping_session.total = 200
        self.shopping_session.save()

        updated_shopping_session = ShoppingSession.objects.get(
            pk=self.shopping_session.pk
        )

        self.assertEqual(updated_shopping_session.total, 200)

    def test_shopping_session_delete(self):
        self.shopping_session.delete()
        self.assertFalse(
            ShoppingSession.objects.filter(pk=self.shopping_session.pk).exists()
        )


class CartItemTestCase(TestCase):
    def setUp(self):
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

        user = get_user_model().objects.create_user(
            username="testuser", email="test@gmail.com", password="testpass"
        )
        self.shopping_session = ShoppingSession.objects.create(user=user)

        self.cart_item = CartItem.objects.create(
            session=self.shopping_session, product=self.product, quantity=2
        )

    def test_cart_item_creation(self):
        self.assertEqual(CartItem.objects.count(), 1)
        self.assertEqual(self.cart_item.session, self.shopping_session)
        self.assertEqual(self.cart_item.product, self.product)
        self.assertEqual(self.cart_item.quantity, 2)

    def test_cart_item_update(self):
        self.cart_item.quantity = 5
        self.cart_item.save()

        updated_cart_item = CartItem.objects.get(pk=self.cart_item.pk)

        self.assertEqual(updated_cart_item.quantity, 5)

    def test_cart_item_delete(self):
        self.cart_item.delete()
        self.assertFalse(CartItem.objects.filter(pk=self.cart_item.pk).exists())