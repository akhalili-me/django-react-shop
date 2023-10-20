from django.urls import path
from rest_framework import routers
from .views import ProductsFilterListView, ProductSearchListView

app_name = "search"

urlpatterns = [
    path(
        "filter/<int:category_id>",
        ProductsFilterListView.as_view(),
        name="filter_products",
    ),
    path("search/<str:q>", ProductSearchListView.as_view(), name="search_products"),
]
