from django.urls import path, include
from rest_framework import routers
from .views import (
    RUDProductView,
    ProductListSortView,
    CategoryListView,
    ProductFeatureListView,
    ProductCommentsListView,
    CommentsCreateView,
    ProductsFilterListView,
    TopSellingProductsEachChildCategoryView,
    CommentLikeCreateView,
    RDCommentLikeView,
    ProductSearchListView
)

app_name = "products"

urlpatterns = [
    path("<int:pk>", RUDProductView.as_view(), name="rud_product"),
    path("list", ProductListSortView.as_view(), name="product_list"),
    path("categories", CategoryListView.as_view(), name="category_list"),
    path(
        "<int:product_id>/features", ProductFeatureListView.as_view(), name="features"
    ),
    path(
        "<int:product_id>/comments", ProductCommentsListView.as_view(), name="comments"
    ),
    path(
        "<int:product_id>/comments/create",
        CommentsCreateView.as_view(),
        name="create_comment",
    ),
    path("filter/<int:category_id>", ProductsFilterListView.as_view(), name="filter"),
    path("search/<str:q>", ProductSearchListView.as_view(), name="search"),
    path(
        "category/<int:pk>",
        TopSellingProductsEachChildCategoryView.as_view(),
        name="child_categories_top_solds",
    ),
    path(
        "commentlike/create/<int:comment_id>",
        CommentLikeCreateView.as_view(),
        name="create_comment_like",
    ),
    path(
        "commentlike/remove/<int:comment_id>",
        RDCommentLikeView.as_view(),
        name="remove_comment_like",
    ),
]
