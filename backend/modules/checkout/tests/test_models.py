from django.test import TestCase
from ..models import Payment
from modules.orders.models import Order
from modules.products.models import Category, Product
from django.contrib.auth import get_user_model
from modules.shipment.models import Address


class PaymentTestCase(TestCase):
    def setUp(self):
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
        self.payment = Payment.objects.create(
            amount=1000, method="Test method", order=self.order
        )

    def test_payment_creation(self):
        self.assertEqual(Payment.objects.count(), 1)
        self.assertEqual(self.payment.amount, 1000)
        self.assertEqual(self.payment.method, "Test method")
        self.assertEqual(self.payment.status, "pending")
        self.assertEqual(self.payment.paid_at, None)
        self.assertEqual(self.payment.order, self.order)

    def test_payment_update(self):
        self.payment.amount = 200
        self.payment.method = "updated method"
        self.payment.save()

        updated_payment = Payment.objects.get(pk=self.payment.pk)

        self.assertEqual(updated_payment.amount, 200)
        self.assertEqual(updated_payment.method, "updated method")

    def test_payment_delete(self):
        self.payment.delete()
        self.assertFalse(Payment.objects.filter(pk=self.payment.pk).exists())
