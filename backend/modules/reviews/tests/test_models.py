from django.contrib.auth import get_user_model
from django.test import TestCase
from modules.products.models import Category, Product
from ..models import Comment, Like, Report
from datetime import timedelta
from django.utils import timezone


class CommentModelTests(TestCase):
    def setUp(self):
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

        self.user = get_user_model().objects.create_user(
            username="testuser", email="test@gmail.com", password="testpass"
        )

        self.comment = Comment.objects.create(
            text="Test comment",
            rate=3,
            author=self.user,
            product=self.product,
        )

    def test_comment_creation(self):
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(self.comment.text, "Test comment")
        self.assertEqual(self.comment.rate, 3)
        self.assertEqual(self.comment.author, self.user)
        self.assertEqual(self.comment.product, self.product)

    def test_comment_update(self):
        self.comment.text = "updated text"
        self.comment.rate = 4
        self.comment.save()

        updated_comment = Comment.objects.get(pk=self.comment.pk)

        self.assertEqual(updated_comment.text, "updated text")
        self.assertEqual(updated_comment.rate, 4)

    def test_comment_delete(self):
        self.comment.delete()

        with self.assertRaises(Comment.DoesNotExist):
            Comment.objects.get(pk=self.comment.pk)


class LikeModelTests(TestCase):
    def setUp(self):
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

        self.user = get_user_model().objects.create_user(
            username="testuser", email="test@gmail.com", password="testpass"
        )

        self.comment = Comment.objects.create(
            text="Test comment",
            rate=3,
            author=self.user,
            product=self.product,
        )

        self.like = Like.objects.create(comment=self.comment, user=self.user)

    def test_like_creation(self):
        self.assertEqual(Like.objects.count(), 1)
        self.assertEqual(self.like.user, self.user)
        self.assertEqual(self.like.comment, self.comment)

    def test_unique_comment_like_constraint(self):
        """Test unique constraint for comment like model by creating an instance the same as in set up method"""
        with self.assertRaises(Exception) as context:
            for i in range(2):
                Like.objects.create(comment=self.comment, user=self.user)
        self.assertTrue("unique_like" in str(context.exception))

    def test_like_update(self):
        new_user = get_user_model().objects.create_user(
            email="test@test.com", username="testuser", password="testpass"
        )

        self.like.user = new_user
        self.like.save()

        updated_comment_like = Like.objects.get(pk=self.like.pk)

        self.assertEqual(updated_comment_like.user, new_user)

    def test_like_delete(self):
        self.like.delete()

        with self.assertRaises(Like.DoesNotExist):
            Like.objects.get(pk=self.like.pk)


class ReportModelTests(TestCase):
    def setUp(self):
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

        self.report = Report.objects.create(
            comment=self.comment1, user=self.user, reason="spam"
        )

    def test_report_creation(self):
        report = Report.objects.create(
            user=self.user, comment=self.comment2, reason="other"
        )
        created_report = Report.objects.get(pk=report.pk)
        self.assertEqual(created_report.comment, self.comment2)
        self.assertEqual(created_report.user, self.user)
        self.assertEqual(created_report.reason, "other")

    def test_report_update(self):
        self.report.reason = "harassment"
        self.report.save()
        updated_report = Report.objects.get(pk=self.report.pk)
        self.assertEqual(updated_report.reason, "harassment")

    def test_report_delete(self):
        self.report.delete()
        self.assertFalse(Report.objects.filter(pk=self.report.pk).exists())

    def test_unique_report(self):
        with self.assertRaises(Exception) as context:
            Report.objects.create(comment=self.comment1, user=self.user, reason="spam")
        self.assertTrue("unique_report" in str(context.exception))

    def test_daily_report_count(self):
        daily_report_count = Report.objects.get_user_today_reports_count(self.user)
        self.assertEqual(daily_report_count, 1)

    def test_past_seven_days_report_count(self):
        four_days_ago = timezone.now() - timedelta(days=4)
        obj = Report.objects.create(
            comment=self.comment2,
            user=self.user,
            reason="spam",
        )
        obj.created_at = four_days_ago
        obj.save()
        past_seven_days_report_count = (
            Report.objects.get_user_past_seven_days_reports_count(self.user)
        )
        self.assertEqual(past_seven_days_report_count, 2)
