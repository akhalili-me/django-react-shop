from rest_framework.permissions import IsAuthenticated
from modules.utility.permissions import IsSuperUserOrObjectOwner
from rest_framework.generics import RetrieveAPIView,ListAPIView,CreateAPIView,DestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .pagination import ProductListPagination, ProductCommentsPagination
from django.http import Http404
from django.db import IntegrityError
from django.core.cache import cache
from .api_exceptions import CommentAlreadyLikedException, SortMethodInvalidException
from .serializers import (
    ProductSerializer,
    ProductCommentCreateSerializer,
    ProductCommentListSerializer,
    FeatureListSerilizer,
    CategorySerializer,
    CommentLikeSerializer,
    TopSellingProductsByChildCategorySerializer,
)
from .models import Product, Comment, Feature, Category, CommentLike
from .helpers import (
    is_sort_invalid,
    get_sort_order,
    filter_products_by_availability,
    filter_products_by_price,
)


class ProductListSortView(ListAPIView):
    serializer_class = ProductSerializer
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


class RUDProductView(RetrieveAPIView):
    serializer_class = ProductSerializer
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


class ProductCommentsListView(ListAPIView):
    serializer_class = ProductCommentListSerializer
    pagination_class = ProductCommentsPagination
    queryset = Comment.objects.all().order_by('-created_at')
    lookup_field = "product_id"


class CommentsCreateView(CreateAPIView):
    serializer_class = ProductCommentCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = get_object_or_404(Product, pk=kwargs.get("product_id"))
        comment = Comment.objects.create(
            product=product, author=request.user, **serializer.validated_data
        )
        return Response(
            {**serializer.data, "id": comment.id}, status=status.HTTP_201_CREATED
        )


class CommentLikeCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs.get("comment_id"))
        try:
            instance = CommentLike.objects.create(comment=comment, user=request.user)
        except IntegrityError:
            raise CommentAlreadyLikedException()
        response_data = CommentLikeSerializer(instance).data
        return Response(response_data, status=status.HTTP_201_CREATED)


class CommentLikeDestroyView(DestroyAPIView):
    permission_classes = [IsSuperUserOrObjectOwner]
    queryset = CommentLike.objects.all()
    lookup_field = "comment__id"
    lookup_url_kwarg = "comment_id"


class ProductsFilterListView(ListAPIView):
    """
    Get products by category and apply filters on it.
    """

    serializer_class = ProductSerializer
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


class TopSellingProductsEachChildCategoryView(ListAPIView):

    serializer_class = TopSellingProductsByChildCategorySerializer

    def get_queryset(self):
        category = get_object_or_404(Category, id=self.kwargs["pk"])

        if category.parent != None:
            raise Http404()

        return category.children.all()


class ProductSearchListView(ListAPIView):

    serializer_class = ProductSerializer
    pagination_class = ProductListPagination

    def get_queryset(self):
        q = self.kwargs.get("q")
        return Product.objects.filter(name__icontains=q).order_by("-views")
    