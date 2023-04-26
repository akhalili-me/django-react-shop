from rest_framework.viewsets import ModelViewSet
from .serializers import UserSerializer, CommentLikeSerializer
from django.contrib.auth import get_user_model
from rest_framework import status, generics
from rest_framework.response import Response
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from products.models import Comment, CommentLike
from django.shortcuts import get_object_or_404
from django.db import IntegrityError

User = get_user_model()


class UserViewSet(ModelViewSet):
    """
    Viewset for creating, editing, deleting and fetching a user.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(self.request.data.get("password"))
        user.save()

    def perform_update(self, serializer):
        user = serializer.save()
        password = self.request.data.get("password")
        if password:
            user.set_password(password)
            user.save()

    def create(self, request, *args, **kwargs):
        """
        Add user and hash the password.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, *args, **kwargs):
        """
        Update user and hash the password.
        """
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class UserCommentsListView(generics.ListAPIView):
    """
    Return the comments associated with the authenticated user.
    """

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user).order_by("-created_at")


class RUDCommentsView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieve, update and destroy comments.
    """

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(
            id=self.kwargs.get("pk"), author=self.request.user
        )


class CommentLikeCreateView(generics.CreateAPIView):
    """
    View for creating comment likes.
    """

    serializer_class = CommentLikeSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = get_object_or_404(Comment, id=kwargs["pk"])

        try:
            serializer.save(user=self.request.user, comment=comment)
        except IntegrityError:
            return Response(
                {"error": "This comment is already liked by this user."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        headers = self.get_success_headers(serializer.data)
        return Response(status=status.HTTP_201_CREATED, headers=headers)


class RDCommentLikeView(generics.RetrieveDestroyAPIView):
    """
    View for retrieve and destroy comment likes.
    """

    serializer_class = CommentLikeSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "comment_id"

    def get_queryset(self):
        return CommentLike.objects.filter(
            user=self.request.user, comment_id=self.kwargs["comment_id"]
        )
    
class AddressViewSet(ModelViewSet):
    """
    View set for retrieve, update, delete and create address.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)