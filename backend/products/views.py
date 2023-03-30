from rest_framework import viewsets, permissions
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *
from rest_framework import generics
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .pagination import ProductListPagination,ProductCommentsPagination
from .permissions import SuperuserEditOnly


class ProductViewSet(ModelViewSet):
    """
    ViewSet for viewing and editing the products.
    """

    serializer_class = ProductSerializer
    pagination_class = ProductListPagination
    permission_classes = [SuperuserEditOnly]

    def get_queryset(self):
        return Product.objects.all().order_by("-created_at")


class ProductImageViewSet(ModelViewSet):
    """
    ViewSet for viewing and editing the product images.
    """

    serializer_class = ProductImageSerializer
    permission_classes = [permissions.IsAuthenticated]

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


class CategoryViewSet(ModelViewSet):
    """
    ViewSet for viewing and editing the categories.
    """

    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class ProductCommentsListView(generics.ListAPIView):
    """
    ViewSet for listing product comments.
    """

    serializer_class = ProductCommentListSerializer
    permission_classes = []
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
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = ProductCommentsPagination

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = get_object_or_404(Product, id=kwargs["product_id"])
        serializer.save(product=product, author=self.request.user)
        product.update_rate()
        headers = self.get_success_headers(serializer.data)
        return Response(status=status.HTTP_201_CREATED, headers=headers)


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

        filter_queries = Q()
        # Price range filter
        if min_price > 0:
            filter_queries &= Q(price__gte=min_price)
        if max_price > 0:
            filter_queries &= Q(price__lte=max_price)

        # Check for product avaiability
        if has_selling_stock == "true":
            filter_queries &= Q(quantity__gte=1)

        queryset = queryset.filter(filter_queries)

        # Order based filter
        sort_queries = {
            "default": queryset,
            "popular": queryset.order_by("-rate"),
            "cheapest": queryset.order_by("price"),
            "most_expensive": queryset.order_by("-price"),
            "newest": queryset.order_by("-created_at"),
        }
        queryset = sort_queries.get(sort)

        return queryset
