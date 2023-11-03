from django.test import TestCase
from modules.orders.models import Order
from ..services import OrderService
from modules.utility.factories import UserFactory, UserAddressFactory, ProductFactory


class OrderTestCase(TestCase):
    def setUp(self):
        # Set up product
        self.user = UserFactory()
        self.address = UserAddressFactory(user=self.user)
        self.product = ProductFactory()
        self.product_quantity_org = self.product.quantity

    def test_proccess_order_method(self):
        order_items_data = [{"product": self.product, "quantity": 1}]
        data = {
            "address": self.address.uuid,
            "shipping_price": 10,
            "total": 1000,
            "payment_method": "Test payment method",
            "order_items": order_items_data,
        }
        order = OrderService.process_order_and_payment(self.user, data)

        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.shipping_price, 10)
        self.assertEqual(order.total, 1000)
        main_payment = order.payments.all().get(is_main_payment=True)
        self.assertEqual(main_payment.amount, data["total"])
        self.assertEqual(main_payment.method, data["payment_method"])
        self.assertEqual(main_payment.status, "pending")

        self.assertEqual(len(order.order_items.all()), len(order_items_data))
        for index, order_item in enumerate(order.order_items.all()):
            self.assertEqual(order_item.product, order_items_data[index]["product"])
            self.assertEqual(order_item.quantity, order_items_data[index]["quantity"])
