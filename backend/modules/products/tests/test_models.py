from django.test import TestCase
from ..models import Product, Category, Comment, ProductImage, CommentLike, Feature
from django.core.files.uploadedfile import SimpleUploadedFile
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


class BaseCommentSetUp(BaseProductSetUp, BaseUserSetUp):
    def setUp(self):
        super().setUp()
        BaseUserSetUp.setUp(self)
        self.comment = Comment.objects.create(
            text="Test Comment", rate=3, author=self.user, product=self.product
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


class CommentTestCase(BaseCommentSetUp):
    def test_comment_creation(self):
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(self.comment.text, "Test Comment")
        self.assertEqual(self.comment.rate, 3)
        self.assertEqual(self.comment.author, self.user)
        self.assertEqual(self.comment.product, self.product)

    def test_update_rate_after_comment_save(self):
        self.assertEqual(self.comment.rate, self.product.rate)


class CommentLikeTestCase(BaseCommentSetUp):
    def setUp(self):
        super().setUp()
        self.comment_like = CommentLike.objects.create(
            comment=self.comment, user=self.user
        )

    def test_comment_like_creation(self):
        self.assertEqual(CommentLike.objects.count(), 1)
        self.assertEqual(self.comment_like.user, self.user)
        self.assertEqual(self.comment_like.comment, self.comment)

    def test_unique_comment_like_constraint(self):
        """Test unique constraint for comment like model by creating an instance the same as in set up method"""
        with self.assertRaises(Exception) as context:
            CommentLike.objects.create(comment=self.comment, user=self.user)
        self.assertTrue("unique_comment_like" in str(context.exception))


class FeatureTestCase(BaseProductSetUp):
    def setUp(self):
        super().setUp()
        self.feature = Feature.objects.create(
            name="Test Feature",
            description="Test feature description",
            product=self.product,
        )

    def test_feature_creation(self):
        self.assertEqual(Feature.objects.count(), 1)
        self.assertEqual(self.feature.name, "Test Feature")
        self.assertEqual(self.feature.description, "Test feature description")
        self.assertEqual(self.feature.product, self.product)
