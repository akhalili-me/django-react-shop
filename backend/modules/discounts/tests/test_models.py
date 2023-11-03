from django.test import TestCase
from ..models import Discount
from django.utils import timezone
from datetime import timedelta

from django.core.exceptions import ValidationError
class DiscountModelTests(TestCase):
    def setUp(self):
        self.discount = Discount.objects.create(
            name="test",
            type="percentage",
            value=20,
            code="TESTCODE",
            expire_at=timezone.now() + timedelta(1),
        )

    def test_discount_creation(self):
        created_discount = Discount.objects.create(
            name="testtest",
            type="fixed",
            value=43,
            code="FFHGS",
            expire_at=timezone.now() + timedelta(3),
        )
        retrieved_discount = Discount.objects.get(pk=created_discount.pk)
        self.assertEqual(retrieved_discount.name, "testtest")
        self.assertEqual(retrieved_discount.type, "fixed")
        self.assertEqual(retrieved_discount.code, "FFHGS")
        self.assertEqual(retrieved_discount.is_active, True)

    def test_discount_percentage_greater_than_one_hundred_validation(self):
        with self.assertRaises(ValidationError):
            Discount.objects.create(
                name="testtest",
                type="percentage",
                value=210,
                code="FFHSFGGS",
                expire_at=timezone.now() + timedelta(3),
            )

    def test_discount_update(self):
        self.discount.code = "SDFSD"
        self.discount.save()
        updated_discount = Discount.objects.get(pk=self.discount.pk)
        self.assertEqual(updated_discount.code, "SDFSD")

    def test_discount_delete(self):
        self.discount.delete()
        self.assertFalse(Discount.objects.filter(pk=self.discount.pk).exists())


# class DiscountUsageModelTests(TestCase):
#     def setUp(self):
#         # Set up product
#         parent_category = Category.objects.create(
#             name="Test Parent",
#             parent=None,
#         )

#         child_category = Category.objects.create(
#             name="Test Child",
#             parent=parent_category,
#         )

#         self.product = Product.objects.create(
#             name="Test Product",
#             category=child_category,
#             description="Test product description",
#             price=20.32,
#             quantity=24,
#         )

#         # Set up order
#         self.user = get_user_model().objects.create_user(
#             username="testuser", email="test@gmail.com", password="testpass"
#         )

#         self.address = Address.objects.create(
#             user=self.user,
#             state="Test State",
#             city="Test City",
#             phone="09012342134",
#             postal_code="1847382365",
#             street_address="Test street address",
#             house_number="434",
#         )

#         self.order = Order.objects.create(
#             user=self.user,
#             address=self.address,
#             shipping_price=10,
#             total=1000,
#         )

#         self.order_item = OrderItem.objects.create(
#             order=self.order, product=self.product, quantity=1
#         )

#     def test_order_item_creation(self):
#         self.assertEqual(OrderItem.objects.count(), 1)
#         self.assertEqual(self.order_item.order, self.order)
#         self.assertEqual(self.order_item.product, self.product)
#         self.assertEqual(self.order_item.quantity, 1)

#     def test_order_item_update(self):
#         self.order_item.quantity = 3
#         self.order_item.save()

#         updated_order_item = OrderItem.objects.get(pk=self.order_item.pk)

#         self.assertEqual(updated_order_item.quantity, 3)

#     def test_order_item_delete(self):
#         self.order_item.delete()
#         self.assertFalse(OrderItem.objects.filter(pk=self.order_item.pk).exists())
