from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from .views import *

from rest_framework import routers

router = routers.DefaultRouter()

router.register(r"users", UserViewSet, basename="users")
router.register(r"address", AddressViewSet, basename="address")

urlpatterns = [
    path("", include(router.urls)),
    path("token", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("comments/", UserCommentsListView.as_view(), name="user_comments"),
    path("comments/<int:pk>", RUDCommentsView.as_view(), name="user_comments_RUD"),
    path(
        "comments/<int:pk>/like/",
        CommentLikeCreateView.as_view(),
        name="create_comment_likes",
    ),
    path(
        "comments/<int:comment_id>/like/remove",
        RDCommentLikeView.as_view(),
        name="retrieve_delete_comment_likes",
    ),
]
