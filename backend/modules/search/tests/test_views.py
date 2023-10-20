from rest_framework.test import APIClient
from django.test import TestCase
from rest_framework import status
from modules.products.models import Category, Product
from django.urls import reverse
from time import sleep
from modules.products.serializers import ProductDetailsSerializer


class ProductFilterTests(TestCase):
    def setUp(self):
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
            name="Test Product1",
            category=child_category,
            description="Test product description",
            price=20.32,
            quantity=90,
            rate=1,
            sold=3,
            views=55,
        )
        sleep(0.5)
        self.product2 = Product.objects.create(
            name="Test Product2",
            category=child_category,
            description="Test product description",
            price=88.01,
            quantity=0,
            rate=3,
            sold=234,
            views=34,
        )
        sleep(0.5)
        self.product3 = Product.objects.create(
            name="Test Product 3",
            category=child_category,
            description="Test product description",
            price=42.01,
            quantity=6,
            rate=2,
            sold=9,
            views=277,
        )
        self.PRODUCT_FILTER_URL = reverse(
            "search:filter_products", args=[child_category.pk]
        )

    def test_product_price_filter(self):
        query_params = {
            "min": "25",
            "max": "89",
        }
        response = self.client.get(self.PRODUCT_FILTER_URL, query_params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = ProductDetailsSerializer(
            [self.product3, self.product2], many=True
        ).data
        self.assertEqual(response.data["results"], expected_data)

    def test_product_availability_filter(self):
        query_params = {
            "has_selling_stock": "true",
        }
        response = self.client.get(self.PRODUCT_FILTER_URL, query_params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = ProductDetailsSerializer(
            [self.product3, self.product1], many=True
        ).data
        self.assertEqual(response.data["results"], expected_data)

    def test_product_sort_filter(self):
        query_params = {
            "sort": "cheapest",
        }
        response = self.client.get(self.PRODUCT_FILTER_URL, query_params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = ProductDetailsSerializer(
            [self.product1, self.product3, self.product2], many=True
        ).data
        self.assertEqual(response.data["results"], expected_data)

    def test_all_product_filters(self):
        query_params = {
            "has_selling_stock": "true",
            "sort": "bestselling",
            "min": "19",
            "max": "50",
        }
        response = self.client.get(self.PRODUCT_FILTER_URL, query_params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = ProductDetailsSerializer(
            [self.product3, self.product1], many=True
        ).data
        self.assertEqual(response.data["results"], expected_data)
