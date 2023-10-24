from django.test import TestCase
from modules.utility.images import create_test_image
from django.contrib.auth import get_user_model
from modules.products.models import Category, Product
from modules.orders.models import Order, OrderItem
from modules.shipment.models import Address
from modules.checkout.models import Payment


class OrderItemSignalTests(TestCase):
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
        self.order = Order.objects.create(
            user=self.user,
            address=self.address,
            shipping_price=10,
            total=1000,
        )
        self.payment = Payment.objects.create(
            amount=1000, method="Test method", order=self.order, is_main_payment=True
        )

        self.order_item = OrderItem.objects.create(
            order=self.order, product=self.product, quantity=1
        )

    def test_update_product_quantity_on_payment_save(self):
        self.payment.status = "paid"
        self.payment.save()
        updated_product = Product.objects.get(pk=self.product.pk)
        self.assertEqual(updated_product.quantity, 23)
