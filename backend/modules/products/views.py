from rest_framework.permissions import IsAuthenticated
from .permissions import SuperuserEditOnly
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .pagination import ProductListPagination, ProductCommentsPagination
from django.http import Http404
from django.db import IntegrityError
from modules.utility.utils.cache import get_data_from_cache
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
    sort_products,
    filter_products_by_availability,
    filter_products_by_price,
)



class ProductListSortView(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def list(self, request):
        sort_method = self.request.query_params.get("sort")

        if is_sort_invalid(sort_method):
            raise SortMethodInvalidException()

        cache_key = f"product_list_{sort_method}"
        data = get_data_from_cache(cache_key)

        if not data:
            self.queryset = sort_products(self.queryset, sort_method)[:6]
            data = super().list(request=request).data
            cache.set(cache_key, data)

        return Response(data)


class RUDProductView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [SuperuserEditOnly]
    queryset = Product.objects.all()


class ProductFeatureListView(generics.ListAPIView):
    """
    Return features associated with a particular product id.
    """

    serializer_class = FeatureListSerilizer

    def get_queryset(self):
        return Feature.objects.filter(product_id=self.kwargs["product_id"])


class CategoryListView(generics.ListAPIView):
    """
    Listing the product categories.
    """

    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def list(self, request):
        cache_key = "category_list"
        data = get_data_from_cache(cache_key)

        if not data:
            data = super().list(request=request).data
            cache.set(cache_key, data)

        return Response(data)


class ProductCommentsListView(generics.ListAPIView):
    """
    ViewSet for listing product comments.
    """

    serializer_class = ProductCommentListSerializer
    pagination_class = ProductCommentsPagination

    def get_queryset(self):
        """
        Return the comments associated with a particular product id.
        """
        product_id = self.kwargs["product_id"]
        return Comment.objects.filter(product_id=product_id).order_by("-created_at")


class CommentsCreateView(generics.CreateAPIView):
    """
    ViewSet for creating comments.
    """

    serializer_class = ProductCommentCreateSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ProductCommentsPagination

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = get_object_or_404(Product, pk=kwargs.get("product_id"))
        Comment.objects.create(
            product=product, author=request.user, **serializer.validated_data
        )
        return Response(status=status.HTTP_201_CREATED)


class CommentLikeCreateView(generics.CreateAPIView):
    """
    View for creating comment likes.
    """

    serializer_class = CommentLikeSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = get_object_or_404(Comment, pk=kwargs.get("pk"))

        try:
            CommentLike.objects.create(comment=comment, user=request.user)
        except IntegrityError:
            raise CommentAlreadyLikedException()

        return Response(status=status.HTTP_201_CREATED)


class RDCommentLikeView(generics.RetrieveDestroyAPIView):
    """
    View for retrieve and destroy comment likes.
    """

    serializer_class = CommentLikeSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "comment_id"

    def get_object(self):
        return get_object_or_404(
            user=self.request.user, comment_id=self.kwargs["comment_id"]
        )


class ProductsFilterListView(generics.ListAPIView):
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
        queryset = Q(category_id=self.kwargs.get("pk"))
        queryset = filter_products_by_price(queryset, min_price, max_price)
        queryset = filter_products_by_availability(queryset, has_selling_stock)

        # Apply filters and sort
        queryset = Product.objects.filter(queryset)
        queryset = sort_products(queryset, sort)

        return queryset


class TopSellingProductsEachChildCategoryView(generics.ListAPIView):
    """
    A view to fetch the top 3 selling product of a child category.
    """

    serializer_class = TopSellingProductsByChildCategorySerializer

    def get_queryset(self):
        category = get_object_or_404(Category, id=self.kwargs["pk"])

        if category.parent != None:
            raise Http404()

        return category.children.all()
