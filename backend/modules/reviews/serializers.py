from modules.products.serializers import ProductSerializer
from rest_framework import serializers
from .models import Comment, Like, Report
from modules.accounts.models import Ban
from .api_exceptions import (
    CommentAlreadyLikedException,
    ReportAlreadyTakenException,
    MaxDailyReportReachedException,
)
from django.utils import timezone
from modules.accounts.api_exceptions import UserBannedForThisActionException
from django.shortcuts import get_object_or_404
from modules.utility.loading import get_model

Product = get_model("products", "Product")


class CommentSerializer(serializers.ModelSerializer):
    product = serializers.SlugField()

    class Meta:
        model = Comment
        fields = ["uuid", "text", "rate", "product"]

    def create(self, validated_data):
        product_slug = validated_data.pop("product")
        product_inst = get_object_or_404(Product, slug=product_slug)
        validated_data["product"] = product_inst
        return super().create(validated_data)


class CommentDetailsSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    total_likes = serializers.SerializerMethodField()

    class Meta(CommentSerializer.Meta):
        fields = [
            "uuid",
            "text",
            "rate",
            "author",
            "total_likes",
        ]

    @staticmethod
    def get_total_likes(obj):
        return obj.likes.count()


class UserCommentsListSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta(CommentSerializer.Meta):
        pass


class LikeSerializer(serializers.ModelSerializer):
    comment = serializers.UUIDField()

    class Meta:
        model = Like
        fields = ["uuid", "comment"]

    def validate(self, attrs):
        comment = get_object_or_404(Comment, uuid=attrs["comment"])
        user = self.context["request"].user

        if Like.objects.filter(comment=comment, user=user).exists():
            raise CommentAlreadyLikedException()

        return attrs

    def create(self, validated_data):
        comment_inst = get_object_or_404(Comment, uuid=validated_data["comment"])
        validated_data["comment"] = comment_inst
        return super().create(validated_data)


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ["uuid", "comment", "reason"]


class ReportCreateSerializer(serializers.ModelSerializer):
    comment = serializers.UUIDField()

    class Meta(ReportSerializer.Meta):
        pass

    def validate(self, attrs):
        super().validate(attrs)
        comment = get_object_or_404(Comment, uuid=attrs.get("comment"))
        user = self.context["request"].user

        self.check_for_existing_report(comment, user)
        self.check_weakly_report_limit_and_apply_user_ban(user)
        self.check_max_daily_reports(user)

        return attrs

    def create(self, validated_data):
        comment_inst = get_object_or_404(Comment, uuid=validated_data["comment"])
        validated_data["comment"] = comment_inst
        return super().create(validated_data)

    def check_for_existing_report(self, comment, user):
        if Report.objects.filter(comment=comment, user=user).exists():
            raise ReportAlreadyTakenException()

    def check_max_daily_reports(self, user):
        reports_in_today = Report.objects.get_user_today_reports_count(user)
        if reports_in_today > 4:
            raise MaxDailyReportReachedException()

    def check_weakly_report_limit_and_apply_user_ban(self, user):
        reports_in_past_seven_days = (
            Report.objects.get_user_past_seven_days_reports_count(user)
        )
        if reports_in_past_seven_days > 15:
            Ban.objects.update_or_create(
                user=user, ban_type="report", banned_until=timezone.now()
            )
            raise UserBannedForThisActionException("report")
