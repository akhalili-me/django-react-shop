from rest_framework.test import APIClient
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from modules.products.models import Category, Product, Feature
from modules.utility.tokens import generate_jwt_token
from django.urls import reverse
from ..serializers import (
    CategorySerializer,
    FeatureListSerilizer,
    ProductDetailsSerializer
)
from time import sleep
from django.core.cache import cache

PRODUCT_LIST_URL = reverse("products:product_list")
CATEGORY_LIST_URL = reverse("products:category_list")


class ProductTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client = APIClient()

        parent_category = Category.objects.create(
            name="Test Parent",
            parent=None,
        )

        child_category = Category.objects.create(
            name="Test Child",
            parent=parent_category,
        )

        self.product1 = Product.objects.create(
            name="Test Product 1",
            category=child_category,
            description="Test product description",
            price=20.32,
            quantity=24,
            sold=55,
            views=58,
        )
        sleep(0.5)
        self.product2 = Product.objects.create(
            name="Test Product 2",
            category=child_category,
            description="Test product description",
            price=5,
            quantity=2,
            sold=88,
            views=45,
        )

        self.user = get_user_model().objects.create_superuser(
            username="testuser", email="test@gmail.com", password="testpass"
        )
        tokens = generate_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')

        self.PRODUCT_RETRIEVE_UPDATE_DELETE_URL = reverse(
            "products:product_retrieve_update_delete", args=[self.product1.pk]
        )

    def test_product_list_fail(self):
        response = self.client.get(PRODUCT_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_products_list_newest_sort(self):
        response = self.client.get(f"{PRODUCT_LIST_URL}?sort=newest")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = ProductDetailsSerializer(
            [self.product2, self.product1], many=True
        ).data
        self.assertEqual(response.data, expected_data)

    def test_products_list_bestselling_sort(self):
        response = self.client.get(f"{PRODUCT_LIST_URL}?sort=bestselling")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = ProductDetailsSerializer(
            [self.product2, self.product1], many=True
        ).data
        self.assertEqual(response.data, expected_data)

    def test_products_list_most_viewed_sort(self):
        response = self.client.get(f"{PRODUCT_LIST_URL}?sort=most_viewed")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = ProductDetailsSerializer(
            [self.product1, self.product2], many=True
        ).data
        self.assertEqual(response.data, expected_data)

    def test_product_retrieve_api(self):
        response = self.client.get(self.PRODUCT_RETRIEVE_UPDATE_DELETE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = ProductDetailsSerializer(self.product1).data
        self.assertEqual(response.data, expected_data)


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


# class TopSoldCategoryProductsTests(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.parent_category = Category.objects.create(
#             name="Test Parent",
#             parent=None,
#         )

#         self.child_category1 = Category.objects.create(
#             name="Test Child 1",
#             parent=self.parent_category,
#         )
#         child_category2 = Category.objects.create(
#             name="Test Child",
#             parent=self.parent_category,
#         )

#         self.product1 = Product.objects.create(
#             name="Test Product1",
#             category=self.child_category1,
#             description="Test product description",
#             price=20.32,
#             quantity=90,
#             rate=1,
#             sold=3,
#             views=55,
#         )
#         self.product2 = Product.objects.create(
#             name="Test Product2",
#             category=child_category2,
#             description="Test product description",
#             price=88.01,
#             quantity=0,
#             rate=3,
#             sold=234,
#             views=34,
#         )
#         self.TOP_SOLD_CHILD_CATEGORY_PRODUCTS = reverse(
#             "products:child_categories_top_solds", args=[self.parent_category.pk]
#         )

#     def test_pass_child_category_instead_of_parent(self):
#         child_category_url = reverse(
#             "products:child_categories_top_solds", args=[self.child_category1.pk]
#         )
#         response = self.client.get(child_category_url)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_retrieve_top_3_sold_products_of_each_child_category(self):
#         response = self.client.get(self.TOP_SOLD_CHILD_CATEGORY_PRODUCTS)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         expected_data = TopSellingProductsByChildCategorySerializer(
#             self.parent_category.children.all(), many=True
#         ).data
#         self.assertEqual(response.data, expected_data)
