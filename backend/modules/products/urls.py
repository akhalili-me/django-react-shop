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
)

urlpatterns = [
    path("<int:pk>", RUDProductView.as_view()),
    path("list", ProductListSortView.as_view()),
    path("categories", CategoryListView.as_view()),
    path("<int:product_id>/features", ProductFeatureListView.as_view()),
    path("<int:product_id>/comments", ProductCommentsListView.as_view()),
    path("<int:product_id>/comments/create", CommentsCreateView.as_view()),
    path("search/<int:pk>", ProductsFilterListView.as_view()),
    path("category/<int:pk>", TopSellingProductsEachChildCategoryView.as_view()),
    path("commentlike/create/<int:pk>", CommentLikeCreateView.as_view()),
    path("commentlike/remove/<int:comment_id>", RDCommentLikeView.as_view()),
]
