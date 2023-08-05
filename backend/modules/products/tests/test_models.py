from django.test import TestCase
from ..models import Product, Category, Comment, ProductImage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
import os
from modules.accounts.tests.test_models import BaseUserSetUp


class BaseTestImageSetUp(TestCase):
    def setUp(self):
        self.test_image_path = os.path.join(os.path.dirname(__file__), "test_image.jpg")

        with open(self.test_image_path, "rb") as f:
            self.test_image = SimpleUploadedFile(
                name="test_image.jpg", content=f.read(), content_type="image/jpeg"
            )


class BaseCategorySetUp(BaseTestImageSetUp):
    def setUp(self):
        super().setUp()
        self.parent_category = Category.objects.create(
            name="Test Parent", parent=None, image=self.test_image
        )
        self.child_category = Category.objects.create(
            name="Test Child", parent=self.parent_category, image=self.test_image
        )


class BaseProductSetUp(BaseCategorySetUp):
    def setUp(self):
        super().setUp()
        self.product = Product.objects.create(
            name="Test Product",
            price=20.32,
            description="Test product description",
            category=self.child_category,
            quantity=24,
        )


class CategoryTestCase(BaseCategorySetUp):
    def test_category_creation(self):
        parent_category = self.parent_category
        child_category = self.child_category

        # Assert counts
        self.assertEqual(Category.objects.count(), 2)

        # Assert properties of objects
        self.assertEqual(parent_category.name, "Test Parent")
        self.assertEqual(parent_category.parent, None)
        self.assertEqual(child_category.name, "Test Child")
        self.assertEqual(child_category.parent, parent_category)
        self.assertTrue(parent_category.image)
        self.assertTrue(child_category.image)


class ProductTestCase(BaseProductSetUp, BaseUserSetUp):
    def test_product_creation(self):
        product = self.product

        self.assertEqual(Product.objects.count(), 1)

        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.description, "Test product description")
        self.assertEqual(product.price, 20.32)
        self.assertEqual(product.category, self.child_category)
        self.assertEqual(product.quantity, 24)
        self.assertEqual(product.rate, 0)
        self.assertEqual(product.views, 0)
        self.assertEqual(product.sold, 0)

    def test_product_update_rate(self):
        BaseUserSetUp.setUp(self)
        for i in range(2):
            Comment.objects.create(
                text="Test Comment", rate=i + 1, author=self.user, product=self.product
            )

        self.product.update_rate()
        self.assertEqual(self.product.rate, 1.5)

    def test_product_update_rate_with_no_comments(self):
        self.product.update_rate()
        self.assertEqual(self.product.rate, 0)


class ProdutImageTestCase(BaseProductSetUp):
    def setUp(self):
        super().setUp()
        self.product_image = ProductImage.objects.create(
            name="Test image", image=self.test_image, product=self.product
        )

    def test_product_image_creation(self):
        self.assertEqual(self.product_image.name, "Test image")
        self.assertEqual(self.product_image.product, self.product)
        self.assertTrue(self.product_image.image)


class CommentTestCase(BaseProductSetUp, BaseUserSetUp):
    def setUp(self):
        super().setUp()
        BaseUserSetUp.setUp(self)
        self.comment = Comment.objects.create(
            text="Test Comment", rate=3, author=self.user, product=self.product
        )

    def test_comment_creation(self):
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(self.comment.text, "Test Comment")
        self.assertEqual(self.comment.rate, 3)
        self.assertEqual(self.comment.author, self.user)
        self.assertEqual(self.comment.product, self.product)
