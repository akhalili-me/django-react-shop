from rest_framework import viewsets,permissions
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q


class ProductViewSet(ModelViewSet):
    """
    ViewSet for viewing and editing the products.
    """
    serializer_class = ProductSerializer
    queryset = Product.objects.none()  # set an empty default queryset

    def get_queryset(self):
        queryset = Product.objects.order_by('-created_at')[:9]
        if self.action == 'retrieve':
            # retrieve single product by id
            queryset = Product.objects.filter(id=self.kwargs['pk'])
        return queryset.select_related('category')

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
        product_id = self.kwargs['product_id']
        return ProductImage.objects.filter(product_id=product_id)
        

class CategoryViewSet(ModelViewSet):
    """
    ViewSet for viewing and editing the categories.
    """
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing the comments.
    """
    serializer_class = CommentSerializer
    def get_queryset(self):
        """
        Return the comments associated with a particular product ID.
        """
        product_id = self.kwargs['product_id']
        return Comment.objects.filter(product_id=product_id)
    

class FilterPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_size = 9


class ProductsFilter(generics.ListAPIView):
    """
    Get products by category and apply filters on it.
    """
    serializer_class = ProductSerializer
    pagination_class = FilterPagination

    def get_queryset(self):
        category_id = self.kwargs.get('pk')
        queryset = Product.objects.filter(category_id=category_id)

        #Get url query parameters
        sort = self.request.query_params.get('sort','default')
        min_price = self.request.query_params.get('min',0)
        max_price = self.request.query_params.get('max',0)
        has_selling_stock = self.request.query_params.get('has_selling_stock',False)

        filter_queries = Q()
        # Price range filter
        if min_price != 0:
            filter_queries &= Q(price__gte=min_price)
        if max_price != 0:
            filter_queries &= Q(price__lte=max_price)

        #Check for product avaiability
        if has_selling_stock:
            filter_queries &= Q(quantity__gte=1)
        
        queryset = queryset.filter(filter_queries)

        #Order based filter
        sort_queries = {
            'default': queryset,
            'popular': queryset.order_by('-rate'),
            'price_ascending': queryset.order_by('price'),
            'price_descending': queryset.order_by('-price'),
        }
        
        queryset = sort_queries.get(sort)

        return queryset
    

