from django.test import TestCase
from ..models import Payment
from modules.utility.factories import OrderFactory 

class PaymentTestCase(TestCase):
    def setUp(self):
        self.order = OrderFactory()
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
