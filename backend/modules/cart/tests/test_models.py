from django.test import TestCase
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
from django.contrib.auth import get_user_model
from modules.products.models import Product, Category
from decimal import Decimal
from django.db import IntegrityError
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


class AddressTestCase(TestCase):
    def setUp(self):
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

    def test_address_update(self):
        self.address.state = "updated state"
        self.address.street_address = "updated street address"
        self.address.save()

        updated_address = Address.objects.get(pk=self.address.pk)

        self.assertEqual(updated_address.state, "updated state")
        self.assertEqual(updated_address.street_address, "updated street address")

    def test_address_delete(self):
        self.address.delete()
        self.assertFalse(Address.objects.filter(pk=self.address.pk).exists())


class PaymentTestCase(TestCase):
    def setUp(self):
        self.payment = Payment.objects.create(
            amount=1000,
            payment_method="Test method",
        )

    def test_payment_creation(self):
        self.assertEqual(Payment.objects.count(), 1)
        self.assertEqual(self.payment.amount, 1000)
        self.assertEqual(self.payment.payment_method, "Test method")
        self.assertEqual(self.payment.status, "pending")
        self.assertEqual(self.payment.paid_at, None)

    def test_payment_update(self):
        self.payment.amount = 200
        self.payment.payment_method = "updated method"
        self.payment.save()

        updated_payment = Payment.objects.get(pk=self.payment.pk)

        self.assertEqual(updated_payment.amount, 200)
        self.assertEqual(updated_payment.payment_method, "updated method")

    def test_payment_delete(self):
        self.payment.delete()
        self.assertFalse(Payment.objects.filter(pk=self.payment.pk).exists())


class OrderTestCase(TestCase):
    def setUp(self):
        # Set up product
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


class OrderItemTestCase(TestCase):
    def setUp(self):
        # Set up product
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

    def test_order_item_creation(self):
        self.assertEqual(OrderItem.objects.count(), 1)
        self.assertEqual(self.order_item.order, self.order)
        self.assertEqual(self.order_item.product, self.product)
        self.assertEqual(self.order_item.quantity, 1)

    def test_order_item_update(self):
        self.order_item.quantity = 3
        self.order_item.save()

        updated_order_item = OrderItem.objects.get(pk=self.order_item.pk)

        self.assertEqual(updated_order_item.quantity, 3)

    def test_order_item_delete(self):
        self.order_item.delete()
        self.assertFalse(OrderItem.objects.filter(pk=self.order_item.pk).exists())


class StateTestCase(TestCase):
    def setUp(self):
        self.state = State.objects.create(name="Test state")

    def test_state_creation(self):
        self.assertEqual(State.objects.count(), 1)
        self.assertEqual(self.state.name, "Test state")

    def test_state_update(self):
        self.state.name = "updated name"
        self.state.save()

        updated_state = State.objects.get(pk=self.state.pk)

        self.assertEqual(updated_state.name, "updated name")

    def test_state_delete(self):
        self.state.delete()
        self.assertFalse(State.objects.filter(pk=self.state.pk).exists())


class CityTestCase(TestCase):
    def setUp(self):
        self.state = State.objects.create(name="Test state")
        self.city = City.objects.create(name="Test city", state=self.state)

    def test_city_creation(self):
        self.assertEqual(City.objects.count(), 1)
        self.assertEqual(self.city.state, self.state)
        self.assertEqual(self.city.name, "Test city")

    def test_city_update(self):
        self.city.name = "updated name"
        self.city.save()

        updated_city = City.objects.get(pk=self.city.pk)

        self.assertEqual(updated_city.name, "updated name")

    def test_city_delete(self):
        self.city.delete()
        self.assertFalse(City.objects.filter(pk=self.city.pk).exists())
