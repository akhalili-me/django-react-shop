from rest_framework.test import APIClient
from django.test import TestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

USER_CREATE_URL = reverse("accounts:register")
TOKEN_OBTAIN_URL = reverse("accounts:token_obtain")
TOKEN_REFRESH_URL = reverse("accounts:token_refresh")


class UserRegisterAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user_api(self):
        payload = {
            "username": "testuser",
            "email": "test1234@gmail.com",
            "password": "Testpassword1@",
        }
        response = self.client.post(USER_CREATE_URL, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), 1)
        user = get_user_model().objects.get(email="test1234@gmail.com")
        self.assertTrue(user.check_password(payload.get("password")))

    def test_create_user_api_invalid_data(self):
        invalid_payload = {
            "email": "test@gmail.com",
            "password": "Testpassword1@",
        }

        response = self.client.post(USER_CREATE_URL, invalid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)

    def test_user_already_exists(self):
        payload = {
            "username": "testuser",
            "email": "test1234@gmail.com",
            "password": "Testpassword1@",
        }
        self.client.post(USER_CREATE_URL, payload, format="json")
        response = self.client.post(USER_CREATE_URL, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_validator(self):
        """
        Test password must contain at least one lowercase letter, one uppercase letter,
        one digit, and be at least 8 characters long
        """
        payload = {
            "username": "testuser",
            "email": "test1234@gmail.com",
            "password": "testpassword",
        }
        response = self.client.post(USER_CREATE_URL, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "password",
            response.data,
        )


class JwtTokenObtainPairTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@gmail.com", username="testuser", password="Test123@"
        )

    def test_jwt_token_obtain_success(self):
        payload = {"email": "test@gmail.com", "password": "Test123@"}
        response = self.client.post(TOKEN_OBTAIN_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_jwt_token_obtain_invalid_credentials(self):
        payload = {"email": "test@gmail.com", "password": "test1234"}
        response = self.client.post(TOKEN_OBTAIN_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_jwt_token_obtan_missing_field(self):
        payload = {"email": "test@gmail.com"}
        response = self.client.post(TOKEN_OBTAIN_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)


class JwtRefreshTokenTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@gmail.com", username="testuser", password="Test123@"
        )

    def test_jwt_refresh_token_success(self):
        payload = {"email": "test@gmail.com", "password": "Test123@"}
        jwt_tokens = self.client.post(TOKEN_OBTAIN_URL, payload).data

        response = self.client.post(
            TOKEN_REFRESH_URL, {"refresh": jwt_tokens["refresh"]}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_jwt_invalid_refresh_token(self):
        payload = {"refresh": "invalid token test"}

        response = self.client.post(TOKEN_REFRESH_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn("access", response.data)
