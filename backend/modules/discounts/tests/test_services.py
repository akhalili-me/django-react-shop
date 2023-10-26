# from rest_framework.test import APIClient
from django.test import TestCase
from ..services import DiscountService
from ..models import Discount, DiscountUsage
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from ..api_exceptions import DiscountInvalidException
from decimal import Decimal
from django.test import TestCase
from modules.products.models import Category, Product
from django.contrib.auth import get_user_model
from modules.shipment.models import Address
from modules.orders.models import Order


class DiscountServicesTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            username="testuser", email="test@gmail.com", password="testpass"
        )
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

        self.validated_discount = Discount.objects.create(
            name="test",
            type="percentage",
            value=20,
            code="TESTCODE",
            expire_at=timezone.now() + timedelta(1),
        )

    def test_verify_discount_active_status(self):
        inactive_discount = Discount.objects.create(
            name="test",
            type="percentage",
            value=20,
            code="TESTCODESHJ",
            expire_at=timezone.now() - timedelta(1),
        )
        DiscountService._verify_discount_active_status(self.validated_discount)
        with self.assertRaises(DiscountInvalidException):
            DiscountService._verify_discount_active_status(inactive_discount)

    def test_veriy_discount_has_not_been_used(self):
        DiscountUsage.objects.create(
            user=self.user,
            discount=self.validated_discount,
            amount=25,
            order=self.order,
        )
        with self.assertRaises(DiscountInvalidException):
            DiscountService._verify_discount_not_previously_used(
                self.validated_discount, self.user
            )

    def test_verify_user_validity_user(self):
        new_user = get_user_model().objects.create_superuser(
            username="testtestuser", email="testtest@gmail.com", password="testpass"
        )
        user_discount = Discount.objects.create(
            name="test",
            type="percentage",
            value=20,
            code="TESTCODESGH",
            expire_at=timezone.now() + timedelta(1),
            user=self.user,
        )
        with self.assertRaises(DiscountInvalidException):
            DiscountService._verify_discount_user_validity(user_discount, new_user)

    def test_apply_discount_service(self):
        final_price = DiscountService.apply_discount(self.validated_discount, 968)
        self.assertEqual(final_price, Decimal("774.40"))

    def test_calculate_discount_amount(self):
        discount_amount = DiscountService.calculate_discount_amount(
            self.validated_discount, 543
        )
        self.assertEqual(discount_amount, Decimal("108.6"))
