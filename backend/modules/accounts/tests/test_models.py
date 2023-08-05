from django.contrib.auth import get_user_model
from django.test import TestCase


class BaseUserSetUp(TestCase):
    def setUp(self):
        email = "test@gmail.com"
        password = "testpass"
        username = "Test Username"
        self.user = get_user_model().objects.create_user(email, password, username)


class UserTestCase(BaseUserSetUp):
    def test_user_creation(self):
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(self.user.email, "test@gmail.com")
        self.assertEqual(self.user.username, "Test Username")
        self.assertTrue(self.user.check_password("testpass"))
