from django.test import TestCase
from ..services import DiscountService
from ..models import Discount, DiscountUsage
from django.utils import timezone
from datetime import timedelta
from ..api_exceptions import DiscountInvalidException
from decimal import Decimal
from django.test import TestCase
from modules.utility.factories import OrderFactory, UserFactory


class DiscountServicesTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.order = OrderFactory(user=self.user)
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
        new_user = UserFactory()
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
