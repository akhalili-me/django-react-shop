from rest_framework.test import APIClient
from django.test import TestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model


class UserRegisterAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("accounts:register")

    def test_create_user_api(self):
        payload = {
            "username": "testuser",
            "email": "test1234@gmail.com",
            "password": "Testpassword1@",
        }
        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertTrue(get_user_model().objects.filter(username="testuser").exists())

    def test_create_user_api_invalid_data(self):
        invalid_payload = {
            "password": "testpassword",
        }

        response = self.client.post(self.url, invalid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)
