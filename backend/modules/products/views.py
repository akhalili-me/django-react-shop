from rest_framework.generics import (
    RetrieveAPIView,
    ListAPIView,
)
from rest_framework.response import Response
from django.core.cache import cache
from .api_exceptions import SortMethodInvalidException
from .serializers import (
    ProductDetailsSerializer,
    FeatureListSerilizer,
    CategorySerializer,
)
from .models import Product, Feature, Category
from .helpers import (
    is_sort_invalid,
    get_sort_order,
)


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


class ProductRetrieveView(RetrieveAPIView):
    serializer_class = ProductDetailsSerializer
    queryset = Product.objects.all()


class ProductFeatureListView(ListAPIView):
    """
    Return features associated with a particular product id.
    """

    serializer_class = FeatureListSerilizer

    def get_queryset(self):
        return Feature.objects.filter(product_id=self.kwargs["product_id"])


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
