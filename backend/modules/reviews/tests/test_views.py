from rest_framework.test import APIClient
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from modules.products.models import Category, Product
from modules.accounts.models import Ban
from modules.utility.tokens import generate_jwt_token
from django.urls import reverse
from time import sleep
from ..models import Comment, Like, Report
from ..serializers import (
    UserCommentsListSerializer,
    CommentDetailsSerializer,
    CommentSerializer,
)

USER_COMMENTS_LIST_URL = reverse("reviews:user_comments")
COMMENT_CREATE_URL = reverse("reviews:comment_create")
LIKE_CREATE_URL = reverse("reviews:like_create")
REPORT_CREATE_URL = reverse("reviews:report_create")


class CommentViewsTests(TestCase):
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
        sleep(0.5)
        self.comment2 = Comment.objects.create(
            text="Test comment 2",
            rate=2,
            author=self.user,
            product=self.product,
        )
        tokens = generate_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
        self.COMMENT_1_RETRIEVE_UPDATE_DELETE_URL = reverse(
            "reviews:comment_retrieve_update_delete", args=[self.comment1.pk]
        )

    def test_user_comments_list_api(self):
        response = self.client.get(USER_COMMENTS_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        expected_data = UserCommentsListSerializer(
            [self.comment2, self.comment1], many=True
        ).data
        self.assertEqual(response.data["results"], expected_data)

    def test_product_comments_list_api(self):
        PRODUCT_COMMENTS_LIST_URL = reverse(
            "reviews:product_comments", args=[self.product.pk]
        )
        response = self.client.get(PRODUCT_COMMENTS_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = CommentDetailsSerializer(
            [self.comment2, self.comment1], many=True
        ).data
        self.assertEqual(response.data["results"], expected_data)

    def test_comment_create_api(self):
        payload = {"text": "test comment", "rate": 3, "product": self.product.pk}
        response = self.client.post(COMMENT_CREATE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Comment.objects.filter(pk=response.data["id"]).exists())

    def test_comment_retrieve_api(self):
        response = self.client.get(self.COMMENT_1_RETRIEVE_UPDATE_DELETE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = CommentSerializer(self.comment1).data
        self.assertEqual(response.data, expected_data)

    def test_comment_update_api(self):
        payload = {"rate": 5}
        response = self.client.patch(self.COMMENT_1_RETRIEVE_UPDATE_DELETE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # TODO

    def test_comment_delete_api(self):
        response = self.client.delete(self.COMMENT_1_RETRIEVE_UPDATE_DELETE_URL)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comment.objects.filter(pk=self.comment1.pk).exists())

    def test_comment_owner_permission(self):
        new_user = get_user_model().objects.create_user(
            username="testtestuser", email="testtest@gmail.com", password="testpass"
        )
        tokens = generate_jwt_token(new_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
        response = self.client.delete(self.COMMENT_1_RETRIEVE_UPDATE_DELETE_URL)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class LikeViewsTests(TestCase):
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
            text="Test comment1",
            rate=3,
            author=self.user,
            product=self.product,
        )
        self.comment2 = Comment.objects.create(
            text="Test comment2",
            rate=3,
            author=self.user,
            product=self.product,
        )

        self.like = Like.objects.create(comment=self.comment2, user=self.user)
        tokens = generate_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')

    def test_like_create_api(self):
        payload = {"comment": self.comment1.pk}
        response = self.client.post(LIKE_CREATE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Like.objects.filter(pk=response.data["id"]).exists())

    def test_like_delete_api(self):
        Like_DELETE_URL = reverse("reviews:like_delete", args=[self.comment2.pk])
        response = self.client.delete(Like_DELETE_URL)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Like.objects.filter(user=self.user, comment=self.comment2).exists()
        )

    def test_unique_like_validation(self):
        payload = {"comment": self.comment2.pk}
        response = self.client.post(LIKE_CREATE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["detail"], "Comment is already liked by current user."
        )


class ReportViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="testuser", email="test@gmail.com", password="testpass"
        )
        tokens = generate_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')

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

        for i in range(20):
            comment = Comment.objects.create(
                text="Test comment",
                rate=4,
                author=self.user,
                product=self.product,
            )
            setattr(self, f"comment{i+1}", comment)

        self.report = Report.objects.create(
            comment=self.comment1, user=self.user, reason="spam"
        )
        self.REPORT_RETRIEVE_UPDATE_DESTROY_URL = reverse(
            "reviews:report_retrieve_update_delete", args=[self.report.pk]
        )

    def test_report_create_api(self):
        payload = {"comment": self.comment2.pk, "reason": "spam"}
        response = self.client.post(REPORT_CREATE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Report.objects.filter(pk=response.data["id"]).exists())

    def test_report_update_api(self):
        payload = {"reason": "inappropriate content"}
        response = self.client.patch(self.REPORT_RETRIEVE_UPDATE_DESTROY_URL, payload)
        updated_report = Report.objects.get(pk=self.report.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_report.reason, "inappropriate content")

    def test_report_delete_api(self):
        response = self.client.delete(self.REPORT_RETRIEVE_UPDATE_DESTROY_URL)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Report.objects.filter(pk=self.report.pk).exists())

    def test_unique_report(self):
        payload = {"comment": self.comment1.pk, "reason": "spam"}
        response = self.client.post(REPORT_CREATE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["detail"], "Report has already been taken by current user."
        )

    def test_max_daily_report_limit(self):
        for i in range(4):
            comment = getattr(self, f"comment{i+2}")
            Report.objects.create(comment=comment, user=self.user, reason="spam")
        payload = {"comment": self.comment8.pk, "reason": "spam"}
        response = self.client.post(REPORT_CREATE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"], "You have reached the daily limit of reports."
        )

    def test_user_ban_after_report_limit_reach(self):
        for i in range(15):
            comment = getattr(self, f"comment{i+2}")
            Report.objects.create(comment=comment, user=self.user, reason="spam")
        payload = {"comment": self.comment20.pk, "reason": "spam"}
        response = self.client.post(REPORT_CREATE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"], "User is banned for report actions.")
        self.assertTrue(Ban.objects.filter(ban_type="report", user=self.user).exists())
