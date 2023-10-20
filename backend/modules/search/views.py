from rest_framework.generics import ListAPIView
from django.db.models import Q
from modules.products.models import Product
from modules.products.serializers import ProductDetailsSerializer
from modules.products.pagination import ProductListPagination
from .helpers import filter_products_by_availability, filter_products_by_price
from modules.products.helpers import get_sort_order


class ProductSearchListView(ListAPIView):
    serializer_class = ProductDetailsSerializer
    pagination_class = ProductListPagination

    def get_queryset(self):
        q = self.kwargs.get("q")
        return Product.objects.filter(name__icontains=q).order_by("-views")


class ProductsFilterListView(ListAPIView):
    """
    Get products by category and apply filters on it.
    """

    serializer_class = ProductDetailsSerializer
    pagination_class = ProductListPagination

    def get_queryset(self):
        # Get url query parameters
        sort = self.request.query_params.get("sort", "default")
        min_price = int(self.request.query_params.get("min", 0))
        max_price = int(self.request.query_params.get("max", 0))
        has_selling_stock = self.request.query_params.get("has_selling_stock", "false")

        # Get Q objects
        queryset = Q(category_id=self.kwargs.get("category_id"))
        queryset = filter_products_by_price(queryset, min_price, max_price)
        queryset = filter_products_by_availability(queryset, has_selling_stock)

        # Apply filters and sort
        queryset = Product.objects.filter(queryset)
        queryset = queryset.order_by(get_sort_order(sort))

        return queryset
