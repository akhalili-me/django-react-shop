from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    DestroyAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    CommentDetailsSerializer,
    UserCommentsListSerializer,
    CommentSerializer,
    LikeSerializer,
    ReportSerializer,
)
from .models import Comment, Like, Report
from .pagination import CommentsPagination
from modules.utility.permissions import IsSuperUserOrObjectOwner
from django.shortcuts import get_object_or_404
from modules.accounts.mixins import BanCheckMixin


class UserCommentsListView(ListAPIView):
    serializer_class = UserCommentsListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CommentsPagination

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user).order_by("-created_at")


class ProductCommentsListView(ListAPIView):
    serializer_class = CommentDetailsSerializer
    pagination_class = CommentsPagination

    def get_queryset(self):
        return Comment.objects.filter(
            product_id=self.kwargs.get("product_id")
        ).order_by("-created_at")


class CommentCreateView(CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsSuperUserOrObjectOwner]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    user_field = "author"


class LikeCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LikeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LikeDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        like = get_object_or_404(
            Like, comment_id=self.kwargs["comment_id"], user=self.request.user
        )
        return like


class ReportCreateView(BanCheckMixin, CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReportSerializer
    ban_type = "report"

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReportRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsSuperUserOrObjectOwner]
    serializer_class = ReportSerializer
    queryset = Report.objects.all()
