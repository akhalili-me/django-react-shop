from rest_framework.test import APIClient
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from modules.products.models import Category, Product, Feature, Comment, CommentLike
from modules.utility.images import create_test_image
from modules.utility.tokens import generate_jwt_token
from django.urls import reverse
from ..serializers import (
    ProductSerializer,
    CategorySerializer,
    FeatureListSerilizer,
    ProductCommentListSerializer,
)
from django.core.cache import cache
from datetime import datetime, timedelta

PRODUCT_LIST_URL = reverse("products:product_list")
CATEGORY_LIST_URL = reverse("products:category_list")


class ProductTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client = APIClient()

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

        self.product1 = Product.objects.create(
            name="Test Product 1",
            category=child_category,
            description="Test product description",
            price=20.32,
            quantity=24,
            sold=55,
            views=58,
            created_at=datetime.now() - timedelta(days=2),
        )
        self.product2 = Product.objects.create(
            name="Test Product 2",
            category=child_category,
            description="Test product description",
            price=5,
            quantity=2,
            sold=88,
            views=45,
            created_at=datetime.now() - timedelta(days=1),
        )

        self.user = get_user_model().objects.create_superuser(
            username="testuser", email="test@gmail.com", password="testpass"
        )
        tokens = generate_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')

        self.RUD_PRODUCT_URL = reverse("products:rud_product", args=[self.product1.pk])

    def test_product_list_fail(self):
        response = self.client.get(PRODUCT_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_products_list_newest_sort(self):
        response = self.client.get(f"{PRODUCT_LIST_URL}?sort=newest")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = ProductSerializer(
            [self.product2, self.product1], many=True
        ).data
        self.assertEqual(response.data, expected_data)

    def test_products_list_bestselling_sort(self):
        response = self.client.get(f"{PRODUCT_LIST_URL}?sort=bestselling")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = ProductSerializer(
            [self.product2, self.product1], many=True
        ).data
        self.assertEqual(response.data, expected_data)

    def test_products_list_most_viewed_sort(self):
        response = self.client.get(f"{PRODUCT_LIST_URL}?sort=most_viewed")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = ProductSerializer(
            [self.product1, self.product2], many=True
        ).data
        self.assertEqual(response.data, expected_data)

    def test_product_retrieve_api(self):
        response = self.client.get(self.RUD_PRODUCT_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = ProductSerializer(self.product1).data
        self.assertEqual(response.data, expected_data)

    def test_product_update_api(self):
        payload = {"name": "updated name", "price": 45}
        response = self.client.patch(self.RUD_PRODUCT_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_product = Product.objects.get(pk=self.product1.pk)
        self.assertEqual(updated_product.name, "updated name")
        self.assertEqual(updated_product.price, 45)

    def test_product_delete_api(self):
        response = self.client.delete(self.RUD_PRODUCT_URL)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(pk=self.product1.pk).exists())


class CategoryTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client = APIClient()

        self.parent_category = Category.objects.create(
            name="Test Parent",
            parent=None,
        )

        self.child_category = Category.objects.create(
            name="Test Child",
            parent=self.parent_category,
        )

    def test_category_list_api(self):
        response = self.client.get(CATEGORY_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = CategorySerializer(
            [self.parent_category, self.child_category], many=True
        ).data
        self.assertEqual(response.data, expected_data)


class FeatureTests(TestCase):
    def setUp(self):
        self.client = APIClient()
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

        self.feature1 = Feature.objects.create(
            name="Test Feature 1",
            description="Test feature 1 description",
            product=self.product,
        )
        self.feature2 = Feature.objects.create(
            name="Test Feature 2",
            description="Test feature 2 description",
            product=self.product,
        )
        self.PRODUCT_FEATURES_LIST_URL = reverse(
            "products:features", args=[self.product.pk]
        )

    def test_product_features_list_api(self):
        response = self.client.get(self.PRODUCT_FEATURES_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = FeatureListSerilizer(
            [self.feature1, self.feature2], many=True
        ).data
        self.assertEqual(response.data, expected_data)


class ProductCommentTests(TestCase):
    def setUp(self):
        self.client = APIClient()
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
            rate=2,
            author=self.user,
            product=self.product,
        )

        self.PRODUCT_COMMENTS_LIST_URL = reverse(
            "products:comments", args=[self.product.pk]
        )
        tokens = generate_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')

        self.CREATE_COMMENT_URL = reverse(
            "products:create_comment", args=[self.product.id]
        )

    def test_product_comment_list_api(self):
        response = self.client.get(self.PRODUCT_COMMENTS_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = ProductCommentListSerializer(
            [self.comment2, self.comment1], many=True
        ).data
        self.assertEqual(response.data["results"], expected_data)

    def test_liked_by_current_user_field(self):
        CommentLike.objects.create(comment=self.comment1, user=self.user)
        response = self.client.get(self.PRODUCT_COMMENTS_LIST_URL)
        self.assertTrue(response.data["results"][1]["liked_by_current_user"])

    def test_comment_create_api(self):
        payload = {"text": "test comment", "rate": 3}
        response = self.client.post(self.CREATE_COMMENT_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Comment.objects.filter(pk=response.data["id"]).exists())


class CommentLikeTests(TestCase):
    def setUp(self):
        self.client = APIClient()
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
        tokens = generate_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')

        self.comment = Comment.objects.create(
            text="Test comment",
            rate=3,
            author=self.user,
            product=self.product,
        )
        self.COMMENT_LIKE_CREATE_URL = reverse(
            "products:create_comment_like", args=[self.comment.id]
        )

    def test_comment_like_create_api(self):
        response = self.client.post(self.COMMENT_LIKE_CREATE_URL)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        comment_like = CommentLike.objects.get(pk=response.data["id"])
        self.assertEqual(comment_like.user, self.user)
        self.assertEqual(comment_like.comment, self.comment)