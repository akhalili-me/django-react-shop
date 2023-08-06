from django.test import TestCase
from modules.accounts.tests.test_models import BaseUserSetUp
from modules.products.tests.test_models import BaseProductSetUp
from ..models import ShoppingSession, CartItem
from decimal import Decimal


class BaseShoppingSessionSetUp(BaseUserSetUp):
    def setUp(self):
        super().setUp()
        self.shopping_session = ShoppingSession.objects.create(user=self.user)


class ShoppingSessionTestCase(BaseShoppingSessionSetUp, BaseProductSetUp):
    def setUp(self):
        super().setUp()
        BaseProductSetUp.setUp(self)

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
