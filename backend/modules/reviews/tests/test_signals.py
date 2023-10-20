from django.contrib.auth import get_user_model
from django.test import TestCase
from modules.products.models import Category, Product
from ..models import Comment, Like, Report
from datetime import timedelta
from django.utils import timezone


class CommentSignalTests(TestCase):
    def setUp(self):
        parent_category = Category.objects.create(
            name="Test Parent",
            parent=None,
        )

        self.child_category = Category.objects.create(
            name="Test Child",
            parent=parent_category,
        )

        self.product = Product.objects.create(
            name="Test Product",
            category=self.child_category,
            description="Test product description",
            price=20.32,
            quantity=24,
        )

        self.user = get_user_model().objects.create_user(
            username="testuser", email="test@gmail.com", password="testpass"
        )

        for i in range(2):
            Comment.objects.create(
                text="Test comment",
                rate=i + 1,
                author=self.user,
                product=self.product,
            )

    def test_product_update_rate(self):
        self.assertEqual(self.product.rate, 1.5)
