from django.urls import path
from .views import (
    ProductReadUpdateDeleteView,
    ProductListSortView,
    CategoryListView,
    FeatureListCreateView,
)

app_name = "products"

urlpatterns = [
    path(
        "<slug:slug>",
        ProductReadUpdateDeleteView.as_view(),
        name="detail",
    ),
    path(
        "<slug:product_slug>/features/",
        FeatureListCreateView.as_view(),
        name="features-list",
    ),
    path("list/", ProductListSortView.as_view(), name="list"),
    path("categories/", CategoryListView.as_view(), name="category-list"),
]
