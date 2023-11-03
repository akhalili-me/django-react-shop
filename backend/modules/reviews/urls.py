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
        "<uuid:uuid>",
        CommentRetrieveUpdateDestroyView.as_view(),
        name="comment-detail",
    ),
    path(
        "product-comments/<slug:product_slug>",
        ProductCommentsListView.as_view(),
        name="product_comments",
    ),
    path("user-comments/", UserCommentsListView.as_view(), name="user_comments"),
    path("create/", CommentCreateView.as_view(), name="comment_create"),
    path("like/create", LikeCreateView.as_view(), name="like_create"),
    path("like/<uuid:comment_uuid>", LikeDeleteView.as_view(), name="like_delete"),
    path("report/", ReportCreateView.as_view(), name="report_create"),
    path(
        "report/<uuid:uuid>",
        ReportRetrieveUpdateDestroyView.as_view(),
        name="report-detail",
    ),
]
