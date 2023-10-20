from django.urls import path
from .views import (
    UserCommentsListView,
    ProductCommentsListView,
    CommentCreateView,
    LikeCreateView,
    CommentRetrieveUpdateDestroyView,
    LikeDeleteView,
    ReportCreateView,
    ReportRetrieveUpdateDestroyView,
)

app_name = "reviews"


urlpatterns = [
    path(
        "<int:pk>",
        CommentRetrieveUpdateDestroyView.as_view(),
        name="comment_retrieve_update_delete",
    ),
    path(
        "product-comments/<int:product_id>",
        ProductCommentsListView.as_view(),
        name="product_comments",
    ),
    path("user-comments/", UserCommentsListView.as_view(), name="user_comments"),
    path("create/", CommentCreateView.as_view(), name="comment_create"),
    path("like/create", LikeCreateView.as_view(), name="like_create"),
    path("like/<int:comment_id>", LikeDeleteView.as_view(), name="like_delete"),
    path("report/", ReportCreateView.as_view(), name="report_create"),
    path(
        "report/<int:pk>",
        ReportRetrieveUpdateDestroyView.as_view(),
        name="report_retrieve_update_delete",
    ),
]
