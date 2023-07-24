from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *
from rest_framework import generics
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .pagination import ProductListPagination, ProductCommentsPagination
from .permissions import SuperuserEditOnly
from django.http import Http404
from .helpers import *
from django.db import IntegrityError


class ProductViewSet(ModelViewSet):
    """
    ViewSet for viewing and editing the products.
    """

    serializer_class = ProductSerializer
    pagination_class = ProductListPagination
    permission_classes = [SuperuserEditOnly]

    def get_queryset(self):
        return Product.objects.all().order_by("-created_at")

    def create(self, request, *args, **kwargs):
        """
        creating a product.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(status=status.HTTP_201_CREATED, headers=headers)


class ProductImageViewSet(ModelViewSet):
    """
    ViewSet for viewing and editing the product images.
    """

    serializer_class = ProductImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return the images associated with a particular product ID.
        """
        product_id = self.kwargs["product_id"]
        return ProductImage.objects.filter(product_id=product_id)


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

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class ProductCommentsCreateView(generics.CreateAPIView):
    """
    ViewSet for creating product comments.
    """

    serializer_class = ProductCommentCreateSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ProductCommentsPagination

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = get_object_or_404(Product, id=kwargs["product_id"])
        serializer.save(product=product, author=self.request.user)
        product.update_rate()
        headers = self.get_success_headers(serializer.data)
        return Response(status=status.HTTP_201_CREATED, headers=headers)


class CommentLikeCreateView(generics.CreateAPIView):
    """
    View for creating comment likes.
    """

    serializer_class = CommentLikeSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            CommentLike.objects.like_comment(kwargs["pk"], request.user)
        except IntegrityError:
            comment_already_liked_response()

        headers = self.get_success_headers(serializer.data)
        return Response(status=status.HTTP_201_CREATED, headers=headers)


class RDCommentLikeView(generics.RetrieveDestroyAPIView):
    """
    View for retrieve and destroy comment likes.
    """

    serializer_class = CommentLikeSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "comment_id"

    def get_queryset(self):
        return CommentLike.objects.filter(
            user=self.request.user, comment_id=self.kwargs["comment_id"]
        )


class ProductsFilterListView(generics.ListAPIView):
    """
    Get products by category and apply filters on it.
    """

    serializer_class = ProductSerializer
    pagination_class = ProductListPagination

    def get_queryset(self):
        category_id = self.kwargs.get("pk")
        queryset = Product.objects.filter(category_id=category_id)

        # Get url query parameters
        sort = self.request.query_params.get("sort", "default")
        min_price = int(self.request.query_params.get("min", 0))
        max_price = int(self.request.query_params.get("max", 0))
        has_selling_stock = self.request.query_params.get("has_selling_stock", "false")

        # Filter products
        queryset = filter_products_by_price(queryset, min_price, max_price)
        queryset = filter_products_by_availability(queryset, has_selling_stock)
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
