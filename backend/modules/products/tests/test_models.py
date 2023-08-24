from django.test import TestCase
from ..models import Product, Category, Comment, ProductImage, CommentLike, Feature
from django.contrib.auth import get_user_model
from modules.utility.images import create_test_image


class CategoryTestCase(TestCase):
    def setUp(self):
        self.parent_category = Category.objects.create(
            name="Test Parent",
            parent=None,
            image=create_test_image(),
        )

        self.child_category = Category.objects.create(
            name="Test Child",
            parent=self.parent_category,
            image=create_test_image(),
        )

    def test_category_creation(self):
        # Assert counts
        self.assertEqual(Category.objects.count(), 2)

        # Assert properties of objects
        self.assertEqual(self.parent_category.name, "Test Parent")
        self.assertEqual(self.parent_category.parent, None)
        self.assertEqual(self.child_category.name, "Test Child")
        self.assertEqual(self.child_category.parent, self.parent_category)
        self.assertTrue(self.parent_category.image)
        self.assertTrue(self.child_category.image)

    def test_category_update(self):
        self.parent_category.name = "updated name"
        self.parent_category.save()

        updated_category = Category.objects.get(pk=self.parent_category.pk)

        self.assertEqual(updated_category.name, "updated name")

    def test_category_delete(self):
        self.child_category.delete()

        with self.assertRaises(Category.DoesNotExist):
            Category.objects.get(pk=self.child_category.id)


class ProductTestCase(TestCase):
    def setUp(self):
        parent_category = Category.objects.create(
            name="Test Parent",
            parent=None,
            image=create_test_image(),
        )

        self.child_category = Category.objects.create(
            name="Test Child",
            parent=parent_category,
            image=create_test_image(),
        )

        self.user = get_user_model().objects.create_user(
            username="testuser", email="test@gmail.com", password="testpass"
        )

        self.product = Product.objects.create(
            name="Test Product",
            category=self.child_category,
            description="Test product description",
            price=20.32,
            quantity=24,
        )

    def test_product_creation(self):
        self.assertEqual(Product.objects.count(), 1)

        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.description, "Test product description")
        self.assertEqual(self.product.price, 20.32)
        self.assertEqual(self.product.category, self.child_category)
        self.assertEqual(self.product.quantity, 24)
        self.assertEqual(self.product.rate, 0)
        self.assertEqual(self.product.views, 0)
        self.assertEqual(self.product.sold, 0)

    def test_product_update_rate(self):
        for i in range(2):
            Comment.objects.create(
                text="Test Comment", rate=i + 1, author=self.user, product=self.product
            )

        self.assertEqual(self.product.rate, 1.5)

    def test_product_update_rate_with_no_comments(self):
        self.product.update_rate()
        self.assertEqual(self.product.rate, 0)

    def test_product_update(self):
        self.product.price = 100
        self.product.quantity = 30
        self.product.save()

        updated_product = Product.objects.get(pk=self.product.pk)

        self.assertEqual(updated_product.price, 100)
        self.assertEqual(updated_product.quantity, 30)

    def test_product_delete(self):
        self.product.delete()

        with self.assertRaises(Product.DoesNotExist):
            Product.objects.get(pk=self.product.pk)


class ProdutImageTestCase(TestCase):
    def setUp(self):
        parent_category = Category.objects.create(
            name="Test Parent",
            parent=None,
            image=create_test_image(),
        )

        self.child_category = Category.objects.create(
            name="Test Child",
            parent=parent_category,
            image=create_test_image(),
        )

        self.product = Product.objects.create(
            name="Test Product",
            category=self.child_category,
            description="Test product description",
            price=20.32,
            quantity=24,
        )

        self.product_image = ProductImage.objects.create(
            name="Test image",
            image=create_test_image(),
            product=self.product,
        )

    def test_product_image_creation(self):
        self.assertEqual(self.product_image.name, "Test image")
        self.assertEqual(self.product_image.product, self.product)
        self.assertTrue(self.product_image.image)

    def test_product_image_update(self):
        self.product_image.name = "updated name"
        self.product_image.save()

        updated_product_image = ProductImage.objects.get(pk=self.product_image.pk)

        self.assertEqual(updated_product_image.name, "updated name")

    def test_product_image_delete(self):
        self.product_image.delete()

        with self.assertRaises(ProductImage.DoesNotExist):
            ProductImage.objects.get(pk=self.product_image.pk)


class CommentTestCase(TestCase):
    def setUp(self):
        parent_category = Category.objects.create(
            name="Test Parent",
            parent=None,
            image=create_test_image(),
        )

        self.child_category = Category.objects.create(
            name="Test Child",
            parent=parent_category,
            image=create_test_image(),
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

        self.comment = Comment.objects.create(
            text="Test comment",
            rate=3,
            author=self.user,
            product=self.product,
        )

    def test_comment_creation(self):
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(self.comment.text, "Test comment")
        self.assertEqual(self.comment.rate, 3)
        self.assertEqual(self.comment.author, self.user)
        self.assertEqual(self.comment.product, self.product)

    def test_product_update_rate(self):
        self.assertEqual(self.comment.rate, self.product.rate)

    def test_comment_update(self):
        self.comment.text = "updated text"
        self.comment.rate = 4
        self.comment.save()

        updated_comment = Comment.objects.get(pk=self.comment.pk)

        self.assertEqual(updated_comment.text, "updated text")
        self.assertEqual(updated_comment.rate, 4)

    def test_comment_delete(self):
        self.comment.delete()

        with self.assertRaises(Comment.DoesNotExist):
            Comment.objects.get(pk=self.comment.pk)


class CommentLikeTestCase(TestCase):
    def setUp(self):
        parent_category = Category.objects.create(
            name="Test Parent",
            parent=None,
            image=create_test_image(),
        )

        self.child_category = Category.objects.create(
            name="Test Child",
            parent=parent_category,
            image=create_test_image(),
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

        self.comment = Comment.objects.create(
            text="Test comment",
            rate=3,
            author=self.user,
            product=self.product,
        )

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
            for i in range(2):
                CommentLike.objects.create(comment=self.comment, user=self.user)
        self.assertTrue("unique_comment_like" in str(context.exception))

    def test_comment_like_update(self):
        new_user = get_user_model().objects.create_user(
            email="test@test.com", username="testuser", password="testpass"
        )

        self.comment_like.user = new_user
        self.comment_like.save()

        updated_comment_like = CommentLike.objects.get(pk=self.comment_like.pk)

        self.assertEqual(updated_comment_like.user, new_user)

    def test_comment_like_delete(self):
        self.comment_like.delete()

        with self.assertRaises(CommentLike.DoesNotExist):
            CommentLike.objects.get(pk=self.comment_like.pk)


class FeatureTestCase(TestCase):
    def setUp(self):
        parent_category = Category.objects.create(
            name="Test Parent",
            parent=None,
            image=create_test_image(),
        )

        self.child_category = Category.objects.create(
            name="Test Child",
            parent=parent_category,
            image=create_test_image(),
        )

        self.product = Product.objects.create(
            name="Test Product",
            category=self.child_category,
            description="Test product description",
            price=20.32,
            quantity=24,
        )

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

    def test_feature_update(self):
        self.feature.name = "updated name"
        self.feature.description = "updated description"
        self.feature.save()

        updated_feature = Feature.objects.get(pk=self.feature.pk)

        self.assertEqual(updated_feature.name, "updated name")
        self.assertEqual(updated_feature.description, "updated description")

    def test_feature_delete(self):
        self.feature.delete()

        with self.assertRaises(Feature.DoesNotExist):
            Feature.objects.get(pk=self.feature.pk)
