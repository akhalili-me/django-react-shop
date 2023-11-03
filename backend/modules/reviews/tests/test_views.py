from rest_framework.test import APIClient
from django.test import TestCase
from rest_framework import status
from modules.accounts.models import Ban
from django.urls import reverse
from time import sleep
from ..models import Comment, Like, Report
from ..serializers import (
    UserCommentsListSerializer,
    CommentDetailsSerializer,
    CommentSerializer,
)
from modules.utility.factories import (
    ProductFactory,
    UserFactory,
    CommentFactory,
    LikeFactory,
    SuperUserFactory,
    ReportFactory,
)
from modules.utility.tokens import apply_jwt_token_credentials_to_client

USER_COMMENTS_LIST_URL = reverse("reviews:user_comments")
COMMENT_CREATE_URL = reverse("reviews:comment_create")
LIKE_CREATE_URL = reverse("reviews:like_create")
REPORT_CREATE_URL = reverse("reviews:report_create")


class CommentViewsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.product = ProductFactory()
        self.user = UserFactory()
        self.comment1 = CommentFactory(product=self.product, author=self.user)
        sleep(0.5)
        self.comment2 = CommentFactory(product=self.product, author=self.user)
        apply_jwt_token_credentials_to_client(self.client, self.user)

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
            "reviews:product_comments", args=[self.product.slug]
        )
        response = self.client.get(PRODUCT_COMMENTS_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = CommentDetailsSerializer(
            [self.comment2, self.comment1], many=True
        ).data
        self.assertEqual(response.data["results"], expected_data)

    def test_comment_create_api(self):
        payload = {"text": "test comment", "rate": 3, "product": self.product.slug}
        response = self.client.post(COMMENT_CREATE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Comment.objects.filter(uuid=response.data["uuid"]).exists())

    def test_comment_retrieve_api(self):
        response = self.client.get(self.comment1.get_absolute_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = CommentSerializer(self.comment1).data
        self.assertEqual(response.data, expected_data)

    def test_comment_update_api(self):
        payload = {"rate": 5}
        response = self.client.patch(self.comment1.get_absolute_url(), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # TODO

    def test_comment_delete_api(self):
        response = self.client.delete(self.comment1.get_absolute_url())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comment.objects.filter(pk=self.comment1.pk).exists())

    def test_comment_owner_permission(self):
        new_user = UserFactory()
        apply_jwt_token_credentials_to_client(self.client, new_user)
        response = self.client.delete(self.comment1.get_absolute_url())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class LikeViewsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.comment1 = CommentFactory()
        self.comment2 = CommentFactory()
        self.like = LikeFactory(comment=self.comment2, user=self.user)
        apply_jwt_token_credentials_to_client(self.client, self.user)

    def test_like_create_api(self):
        payload = {"comment": self.comment1.uuid}
        response = self.client.post(LIKE_CREATE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Like.objects.filter(uuid=response.data["uuid"]).exists())

    def test_like_delete_api(self):
        Like_DELETE_URL = reverse("reviews:like_delete", args=[self.comment2.uuid])
        response = self.client.delete(Like_DELETE_URL)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Like.objects.filter(user=self.user, comment=self.comment2).exists()
        )

    def test_unique_like_validation(self):
        payload = {"comment": self.comment2.uuid}
        response = self.client.post(LIKE_CREATE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["detail"], "Comment is already liked by current user."
        )


class ReportViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.superuser = SuperUserFactory()
        apply_jwt_token_credentials_to_client(self.client, self.superuser)

        for i in range(20):
            comment = CommentFactory()
            setattr(self, f"comment{i+1}", comment)

        self.report = ReportFactory(comment=self.comment1, user=self.user)

    def test_report_create_api(self):
        apply_jwt_token_credentials_to_client(self.client, self.user)
        payload = {"comment": self.comment2.uuid, "reason": "spam"}
        response = self.client.post(REPORT_CREATE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Report.objects.filter(uuid=response.data["uuid"]).exists())

    def test_report_update_api(self):
        payload = {"reason": "inappropriate content"}
        response = self.client.patch(self.report.get_absolute_url(), payload)
        updated_report = Report.objects.get(pk=self.report.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_report.reason, "inappropriate content")

    def test_report_delete_api(self):
        response = self.client.delete(self.report.get_absolute_url())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Report.objects.filter(pk=self.report.pk).exists())

    def test_unique_report(self):
        apply_jwt_token_credentials_to_client(self.client, self.user)
        payload = {"comment": self.comment1.uuid, "reason": "spam"}
        response = self.client.post(REPORT_CREATE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["detail"], "Report has already been taken by current user."
        )

    def test_max_daily_report_limit(self):
        apply_jwt_token_credentials_to_client(self.client, self.user)
        for i in range(4):
            comment = getattr(self, f"comment{i+2}")
            Report.objects.create(comment=comment, user=self.user, reason="spam")

        payload = {"comment": self.comment8.uuid, "reason": "spam"}
        response = self.client.post(REPORT_CREATE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"], "You have reached the daily limit of reports."
        )

    def test_user_ban_after_report_limit_reach(self):
        apply_jwt_token_credentials_to_client(self.client, self.user)
        for i in range(15):
            comment = getattr(self, f"comment{i+2}")
            Report.objects.create(comment=comment, user=self.user, reason="spam")
        payload = {"comment": self.comment20.uuid, "reason": "spam"}
        response = self.client.post(REPORT_CREATE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"], "User is banned for report actions.")
        self.assertTrue(Ban.objects.filter(ban_type="report", user=self.user).exists())
