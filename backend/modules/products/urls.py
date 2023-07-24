from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register("", ProductViewSet, basename="products")
router.register(
    r"(?P<product_id>\d+)/images", ProductImageViewSet, basename="product_images"
)

urlpatterns = [
    path("", include(router.urls)),
    path("categories", CategoryListView.as_view()),
    path("<int:product_id>/features", ProductFeatureListView.as_view()),
    path("<int:product_id>/comments", ProductCommentsListView.as_view()),
    path("<int:product_id>/comments/create", ProductCommentsCreateView.as_view()),
    path("search/<int:pk>", ProductsFilterListView.as_view()),
    path("category/<int:pk>", TopSellingProductsEachChildCategoryView.as_view()),
    path("commentlike/create/<int:pk>",CommentLikeCreateView.as_view()),
    path("commentlike/remove/<int:comment_id>",RDCommentLikeView.as_view())
]
