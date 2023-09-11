from django.test import TestCase
from django.contrib.auth import get_user_model
from modules.products.models import Category, Product, Comment
from django.core.cache import cache


class ProductSignalTests(TestCase):
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

        self.comment1 = Comment.objects.create(
            text="Test comment1",
            rate=3,
            author=self.user,
            product=self.product,
        )

        self.comment2 = Comment.objects.create(
            text="Test comment2",
            rate=4,
            author=self.user,
            product=self.product,
        )

        self.SORT_CHOICES = ("newest", "bestselling", "most_viewed")
        for sort in self.SORT_CHOICES:
            cache.set(f"product_list_{sort}", "sample data")

    def test_product_update_rate_after_comment_creation(self):
        self.assertEqual(self.product.rate, 3.5)

    def test_cache_delete_after_comment_creation(self):
        Comment.objects.create(
            text="Test comment3",
            rate=4,
            author=self.user,
            product=self.product,
        )
        for sort in self.SORT_CHOICES:
            self.assertIsNone(cache.get(f"product_list_{sort}"))

    def test_product_update_rate_after_comment_delete(self):
        self.comment1.delete()
        self.assertEqual(self.product.rate, 4)

    def test_cache_delete_after_comment_delete(self):
        self.comment1.delete()
        for sort in self.SORT_CHOICES:
            self.assertIsNone(cache.get(f"product_list_{sort}"))
