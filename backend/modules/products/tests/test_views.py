from rest_framework.test import APIClient
from django.test import TestCase
from rest_framework import status
from modules.utility.tokens import generate_jwt_token
from django.urls import reverse
from ..serializers import (
    CategorySerializer,
    FeatureSerilizer,
    ProductDetailsSerializer,
)
from time import sleep
from django.core.cache import cache
from modules.utility.factories import (
    ProductFactory,
    UserFactory,
    ChildCategoryFactory,
    FeatureFactory,
    SuperUserFactory,
)

PRODUCT_LIST_URL = reverse("products:list")
CATEGORY_LIST_URL = reverse("products:category-list")


class ProductTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client = APIClient()
        self.product1 = ProductFactory(sold=78, views=333)
        sleep(0.5)
        self.product2 = ProductFactory(sold=255, views=34)
        self.user = UserFactory()
        tokens = generate_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')

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
        response = self.client.get(self.product1.get_absolute_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = ProductDetailsSerializer(self.product1).data
        self.assertEqual(response.data, expected_data)


class CategoryTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client = APIClient()
        self.child_category = ChildCategoryFactory()
        self.parent_category = self.child_category.parent

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
        self.product = ProductFactory()
        self.feature1 = FeatureFactory(product=self.product)
        self.feature2 = FeatureFactory(product=self.product)
        self.PRODUCT_FEATURES_LIST_CREATE_URL = reverse(
            "products:features-list", args=[self.product.slug]
        )

    def test_features_list_api(self):
        response = self.client.get(self.PRODUCT_FEATURES_LIST_CREATE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = FeatureSerilizer([self.feature1, self.feature2], many=True).data
        self.assertEqual(response.data, expected_data)

    def test_feature_create_api(self):
        self.superuser = SuperUserFactory()
        tokens = generate_jwt_token(self.superuser)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
        payload = {"name": "test feature 3", "description": "test description 3"}
        response = self.client.post(self.PRODUCT_FEATURES_LIST_CREATE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
