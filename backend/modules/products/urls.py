from django.urls import path
from .views import (
    ProductRetrieveView,
    ProductListSortView,
    CategoryListView,
    ProductFeatureListView,
)

app_name = "products"

urlpatterns = [
    path(
        "<int:pk>", ProductRetrieveView.as_view(), name="product_retrieve_update_delete"
    ),
    path("list", ProductListSortView.as_view(), name="product_list"),
    path("categories", CategoryListView.as_view(), name="category_list"),
    path(
        "<int:product_id>/features", ProductFeatureListView.as_view(), name="features"
    ),
    # path(
    #     "category/<int:pk>",
    #     TopSellingProductsEachChildCategoryView.as_view(),
    #     name="child_categories_top_solds",
    # ),
]
