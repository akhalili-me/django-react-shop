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
        "<slug:slug>",
        ProductRetrieveView.as_view(),
        name="detail",
    ),
    path(
        "<int:product_id>/features/",
        ProductFeatureListView.as_view(),
        name="features-list",
    ),
    path("list/", ProductListSortView.as_view(), name="list"),
    path("categories/", CategoryListView.as_view(), name="category-list"),
]
