from django.test import TestCase
from modules.utility.images import create_test_image
from django.contrib.auth import get_user_model
from ..models import CartItem, ShoppingSession
from modules.products.models import Category, Product
from decimal import Decimal


class SessionSignalTests(TestCase):
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
            price=20.05,
            quantity=24,
        )

        user = get_user_model().objects.create_user(
            username="testuser", email="test@gmail.com", password="testpass"
        )
        self.shopping_session = ShoppingSession.objects.create(user=user)
        self.cart_item = CartItem.objects.create(
            session=self.shopping_session, product=self.product, quantity=2
        )

    def test_update_session_signal_on_create_cart_item(self):
        expected_total = Decimal(self.cart_item.quantity * self.product.price).quantize(
            Decimal("0.00")
        )
        self.assertEqual(self.shopping_session.total, expected_total)

    def test_update_session_signal_on_delete_cart_item(self):
        initial_total = self.shopping_session.total
        cart_item_price = Decimal(
            self.cart_item.quantity * self.product.price
        ).quantize(Decimal("0.00"))

        self.cart_item.delete()

        self.assertEqual(self.shopping_session.total, initial_total - cart_item_price)
