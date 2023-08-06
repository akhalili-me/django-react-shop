from django.test import TestCase
from modules.accounts.tests.test_models import BaseUserSetUp
from modules.products.tests.test_models import BaseProductSetUp
from ..models import ShoppingSession, CartItem, Address, Payment
from decimal import Decimal
from django.db import IntegrityError


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


class CartItemTestCase(BaseShoppingSessionSetUp, BaseProductSetUp):
    def setUp(self):
        super().setUp()
        BaseProductSetUp.setUp(self)
        self.cart_item = CartItem.objects.create(
            session=self.shopping_session, product=self.product, quantity=2
        )

    def test_cart_item_creation(self):
        self.assertEqual(CartItem.objects.count(), 1)
        self.assertEqual(self.cart_item.session, self.shopping_session)
        self.assertEqual(self.cart_item.product, self.product)
        self.assertEqual(self.cart_item.quantity, 2)


class BaseAddressSetUp(BaseUserSetUp):
    def setUp(self):
        super().setUp()
        self.address = Address.objects.create(
            user=self.user,
            state="Test State",
            city="Test City",
            phone="09012342134",
            postal_code="1847382365",
            street_address="Test street address",
            house_number="434",
        )


class AddressTestCase(BaseAddressSetUp):
    def test_address_creation(self):
        self.assertEqual(Address.objects.count(), 1)
        self.assertEqual(self.address.user, self.user)
        self.assertEqual(self.address.state, "Test State")
        self.assertEqual(self.address.city, "Test City")
        self.assertEqual(self.address.phone, "09012342134")
        self.assertEqual(self.address.postal_code, "1847382365")
        self.assertEqual(self.address.street_address, "Test street address")
        self.assertEqual(self.address.house_number, "434")

    def test_phone_unique_constraint(self):
        with self.assertRaises(IntegrityError):
            Address.objects.create(
                user=self.user,
                state="Test State",
                city="Test City",
                phone="09012342134",
                postal_code="1847382365",
                street_address="Test street address",
                house_number="434",
            )


class BasePaymentSetUp(TestCase):
    def setUp(self):
        self.payment = Payment.objects.create(
            amount=1000,
            payment_method="Test method",
        )


class PaymentTestCase(BasePaymentSetUp):
    def test_payment_creation(self):
        self.assertEqual(Payment.objects.count(), 1)
        self.assertEqual(self.payment.amount, 1000)
        self.assertEqual(self.payment.payment_method, "Test method")
        self.assertEqual(self.payment.status, "pending")
        self.assertEqual(self.payment.paid_at, None)
