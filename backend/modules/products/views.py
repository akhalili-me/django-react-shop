from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
    ListCreateAPIView,
)
from rest_framework.response import Response
from django.core.cache import cache
from .api_exceptions import SortMethodInvalidException
from .serializers import (
    ProductDetailsSerializer,
    FeatureSerilizer,
    CategorySerializer,
)
from .models import Product, Feature, Category
from .helpers import (
    is_sort_invalid,
    get_sort_order,
)
from modules.utility.permissions import IsSuperUserOrReadOnly
from django.shortcuts import get_object_or_404


class ProductListSortView(ListAPIView):
    serializer_class = ProductDetailsSerializer
    queryset = Product.objects.all()

    def list(self, request):
        sort_method = self.request.query_params.get("sort")

        if is_sort_invalid(sort_method):
            raise SortMethodInvalidException()

        cache_key = f"product_list_{sort_method}"
        data = cache.get(cache_key)

        if not data:
            queryset = self.get_queryset().order_by(get_sort_order(sort_method))
            data = self.get_serializer(queryset, many=True).data
            cache.set(cache_key, data)

        return Response(data)


class ProductReadUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsSuperUserOrReadOnly]
    serializer_class = ProductDetailsSerializer
    queryset = Product.objects.all()
    lookup_field = "slug"


class FeatureListCreateView(ListCreateAPIView):
    permission_classes = [IsSuperUserOrReadOnly]
    serializer_class = FeatureSerilizer

    def get_queryset(self):
        return Feature.objects.filter(product__slug=self.kwargs["product_slug"])

    def perform_create(self, serializer):
        product = get_object_or_404(Product, slug=self.kwargs["product_slug"])
        serializer.save(product=product)


class CategoryListView(ListAPIView):
    """
    Listing the product categories.
    """

    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def list(self, request):
        cache_key = "category_list"
        data = cache.get(cache_key)

        if not data:
            data = super().list(request=request).data
            cache.set(cache_key, data)

        return Response(data)


# class TopSellingProductsEachChildCategoryView(ListAPIView):

#     serializer_class = TopSellingProductsByChildCategorySerializer

#     def get_queryset(self):
#         category = get_object_or_404(Category, id=self.kwargs["pk"])

#         if category.parent != None:
#             raise Http404()

#         return category.children.all()
