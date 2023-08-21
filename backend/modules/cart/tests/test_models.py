from django.test import TestCase
from modules.accounts.tests.test_models import BaseUserSetUp
from modules.products.tests.test_models import BaseProductSetUp
from ..models import (
    ShoppingSession,
    CartItem,
    Address,
    Payment,
    Order,
    OrderItem,
    State,
    City,
)
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


class BaseOrderSetUp(BaseAddressSetUp, BasePaymentSetUp):
    def setUp(self):
        super().setUp()
        BasePaymentSetUp.setUp(self)
        self.order = Order.objects.create(
            user=self.user,
            address=self.address,
            payment=self.payment,
            shipping_price=10,
            total=1000,
        )


class OrderTestCase(BaseOrderSetUp, BaseProductSetUp):
    def setUp(self):
        super().setUp()
        BaseProductSetUp.setUp(self)

    def test_order_creation(self):
        """Test default order create method"""
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(self.order.user, self.user)
        self.assertEqual(self.order.address, self.address)
        self.assertEqual(self.order.shipping_price, 10)
        self.assertEqual(self.order.total, 1000)
        self.assertEqual(self.order.payment, self.payment)

    def test_order_payment_order_item_creation_manager_method(self):
        """
        Test order manager method that takes order, payment method
        and order items data and create all of them in database.
        """

        order_data = {"address": self.address, "shipping_price": 10, "total": 1000}
        payment_data = {"amount": 1000, "payment_method": "Test payment method"}
        order_items_data = [{"product": self.product, "quantity": 1}]
        order = Order.objects.create_order_with_payment_and_items(
            self.user, order_data, payment_data, order_items_data
        )

        self.assertEqual(Order.objects.count(), 2)
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.address, self.address)
        self.assertEqual(order.shipping_price, 10)
        self.assertEqual(order.total, 1000)
        self.assertEqual(order.payment.amount, payment_data["amount"])
        self.assertEqual(order.payment.payment_method, payment_data["payment_method"])
        self.assertEqual(order.payment.status, "pending")

        self.assertEqual(len(order.order_items.all()), len(order_items_data))
        for index, order_item in enumerate(order.order_items.all()):
            self.assertEqual(order_item.product, order_items_data[index]["product"])
            self.assertEqual(order_item.quantity, order_items_data[index]["quantity"])
            self.assertEqual(self.product.quantity - order_item.quantity, 23)


class OrderItemTestCase(BaseOrderSetUp, BaseProductSetUp):
    def setUp(self):
        super().setUp()
        BaseProductSetUp.setUp(self)
        self.order_item = OrderItem.objects.create(
            order=self.order, product=self.product, quantity=1
        )

    def test_order_item_creation(self):
        self.assertEqual(OrderItem.objects.count(), 1)
        self.assertEqual(self.order_item.order, self.order)
        self.assertEqual(self.order_item.product, self.product)
        self.assertEqual(self.order_item.quantity, 1)


class StateCityTestCase(TestCase):
    def setUp(self):
        self.state = State.objects.create(name="Test state")
        self.city = City.objects.create(state=self.state, name="Test city")

    def test_state_city_creation(self):
        self.assertEqual(State.objects.count(), 1)
        self.assertEqual(City.objects.count(), 1)
        self.assertEqual(self.state.name, "Test state")
        self.assertEqual(self.city.state, self.state)
        self.assertEqual(self.city.name, "Test city")
