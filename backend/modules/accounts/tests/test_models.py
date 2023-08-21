from django.contrib.auth import get_user_model
from django.test import TestCase


class BaseUserSetUp(TestCase):
    def setUp(self):
        self.email = "test@Gmail.com"
        password = "testpass"
        username = "Test Username"
        self.user = get_user_model().objects.create_user(self.email, password, username)


class UserTestCase(BaseUserSetUp):
    def test_user_creation(self):
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(self.user.email, "test@gmail.com")
        self.assertEqual(self.user.username, "Test Username")
        self.assertTrue(self.user.check_password("testpass"))

    def test_user_email_normalized(self):
        self.assertEqual(self.user.email, self.email.lower())

    def test_user_invalid_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "test pass", "test username")

    def test_super_user_creation(self):
        user = get_user_model().objects.create_superuser(
            "test@yahoo.com", "test pass", "test username"
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
