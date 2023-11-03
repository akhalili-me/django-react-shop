from django.test import TestCase
from modules.utility.factories import PaymentFactory, OrderItemFactory
from modules.products.models import Product


class OrderItemSignalTests(TestCase):
    def setUp(self):
        self.order_item = OrderItemFactory()
        self.product = self.order_item.product
        payment_kwargs = {
            "order": self.order_item.order,
            "status": "pending",
            "paid_at": None,
        }
        self.payment = PaymentFactory(**payment_kwargs)

    def test_update_product_quantity_on_payment_save(self):
        self.payment.status = "paid"
        self.payment.save()
        updated_product = Product.objects.get(pk=self.product.pk)
        expected_quantity = self.product.quantity - self.order_item.quantity
        self.assertEqual(updated_product.quantity, expected_quantity)
        self.assertEqual(self.payment.order.status, "complete")
