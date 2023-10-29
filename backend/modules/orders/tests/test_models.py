from django.test import TestCase
from modules.products.models import Category, Product
from modules.orders.models import Order, OrderItem
from modules.checkout.models import Payment
from modules.shipment.models import Address
from django.contrib.auth import get_user_model


class OrderTestCase(TestCase):
    def setUp(self):
        # Set up product
        parent_category = Category.objects.create(
            name="Test Parent",
            parent=None,
        )

        child_category = Category.objects.create(
            name="Test Child",
            parent=parent_category,
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

        self.order = Order.objects.create(
            user=self.user,
            address=self.address,
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

    def test_order_update(self):
        pass

    def test_order_delete(self):
        pass

class OrderItemTestCase(TestCase):
    def setUp(self):
        # Set up product
        parent_category = Category.objects.create(
            name="Test Parent",
            parent=None,
        )

        child_category = Category.objects.create(
            name="Test Child",
            parent=parent_category,
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

        self.order = Order.objects.create(
            user=self.user,
            address=self.address,
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
