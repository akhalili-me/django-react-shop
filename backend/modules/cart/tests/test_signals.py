from django.test import TestCase
from decimal import Decimal
from modules.utility.factories import (
    ShoppingSessionFactory,
    CartItemFactory,
)


class SessionSignalTests(TestCase):
    def setUp(self):
        self.shopping_session = ShoppingSessionFactory()
        self.cart_item = CartItemFactory(session=self.shopping_session)

    def test_update_session_signal_on_create_cart_item(self):
        expected_total = Decimal(
            self.cart_item.quantity * self.cart_item.product.price
        ).quantize(Decimal("0.00"))
        self.assertEqual(self.shopping_session.total, expected_total)

    def test_update_session_signal_on_delete_cart_item(self):
        initial_total = self.shopping_session.total
        cart_item_price = Decimal(
            self.cart_item.quantity * self.cart_item.product.price
        ).quantize(Decimal("0.00"))

        self.cart_item.delete()

        self.assertEqual(self.shopping_session.total, initial_total - cart_item_price)
