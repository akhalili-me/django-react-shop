from django.test import TestCase
from modules.orders.models import Order, OrderItem
from modules.utility.factories import (
    UserFactory,
    BillingAddressFactory,
    OrderFactory,
    ProductFactory,
)


class OrderTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.address = BillingAddressFactory()
        self.order = Order.objects.create(
            user=self.user,
            billing_address=self.address,
            shipping_price=10,
            total=1000,
        )

    def test_order_creation(self):
        """Test default order create method"""
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(self.order.user, self.user)
        self.assertEqual(self.order.billing_address, self.address)
        self.assertEqual(self.order.shipping_price, 10)
        self.assertEqual(self.order.total, 1000)

    def test_order_update(self):
        pass

    def test_order_delete(self):
        pass


class OrderItemTestCase(TestCase):
    def setUp(self):
        self.order = OrderFactory()
        self.product = ProductFactory()
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
