from rest_framework.test import APIClient
from django.test import TestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from modules.products.models import Category, Product, Comment
from modules.utility.images import create_test_image
from modules.utility.tokens import generate_jwt_token
from ..serializers import UserCommentsSerializer, CommentSerializer, AddressSerializer
from modules.cart.models import Address

USER_CREATE_URL = reverse("accounts:register")
TOKEN_OBTAIN_URL = reverse("accounts:token_obtain")
TOKEN_REFRESH_URL = reverse("accounts:token_refresh")
USER_COMMENTS_LIST_URL = reverse("accounts:user_comments")
ADDRESS_LIST_CREATE_URL = reverse("accounts:address-list")


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


class CommentViewsTests(TestCase):
    def setUp(self):
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

        self.product = Product.objects.create(
            name="Test Product",
            category=child_category,
            description="Test product description",
            price=20.32,
            quantity=24,
        )

        self.user = get_user_model().objects.create_user(
            username="testuser", email="test@gmail.com", password="testpass"
        )

        self.comment1 = Comment.objects.create(
            text="Test comment 1",
            rate=4,
            author=self.user,
            product=self.product,
        )
        self.comment2 = Comment.objects.create(
            text="Test comment 2",
            rate=2,
            author=self.user,
            product=self.product,
        )
        tokens = generate_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
        self.RUD_COMMENT_1_URL = reverse(
            "accounts:user_comments_RUD", args=[self.comment1.pk]
        )

    def test_list_user_comments_api(self):
        response = self.client.get(USER_COMMENTS_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        expected_data = UserCommentsSerializer(
            [self.comment2, self.comment1], many=True
        ).data
        self.assertEqual(response.data["results"], expected_data)

    def test_comment_retrieve_api(self):
        response = self.client.get(self.RUD_COMMENT_1_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = CommentSerializer(self.comment1).data
        self.assertEqual(response.data, expected_data)

    def test_comment_update_api(self):
        payload = {"rate": 5}
        response = self.client.patch(self.RUD_COMMENT_1_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        comment = Comment.objects.get(pk=self.comment1.pk)
        self.assertEqual(comment.rate, 5)

    def test_comment_delete_api(self):
        response = self.client.delete(self.RUD_COMMENT_1_URL)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comment.objects.filter(pk=self.comment1.pk).exists())


class AddressViewsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", email="test@gmail.com", password="testpass"
        )
        self.client = APIClient()
        tokens = generate_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')

        self.address = Address.objects.create(
            user=self.user,
            state="Test State",
            city="Test City",
            phone="09012342134",
            postal_code="1847382365",
            street_address="Test street address",
            house_number="434",
        )

    def test_list_user_address_api(self):
        response = self.client.get(ADDRESS_LIST_CREATE_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = AddressSerializer([self.address], many=True).data
        self.assertEqual(response.data, expected_data)

    def test_address_create_api(self):
        payload = {
            "user": self.user,
            "state": "Test State",
            "city": "Test City",
            "phone": "09012452123",
            "postal_code": "1847382365",
            "street_address": "Test street address",
            "house_number": "434",
        }
        response = self.client.post(ADDRESS_LIST_CREATE_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Address.objects.count(), 2)
        self.assertTrue(Address.objects.filter(phone="09012452123").exists())

    def test_address_retrieve_api(self):
        pass

    def test_address_update_api(self):
        pass

    def test_address_delete_api(self):
        pass
