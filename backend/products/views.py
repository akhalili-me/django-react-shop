from rest_framework import viewsets,permissions
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *
from rest_framework import generics
from django.db.models import F
from rest_framework.pagination import PageNumberPagination
from itertools import chain

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
        query = Product.objects.filter(category_id=category_id)

        #Get url query parameters
        order = self.request.query_params.get('order','default')
        min_price = self.request.query_params.get('min',0)
        max_price = self.request.query_params.get('max',0)
        has_selling_stock = self.request.query_params.get('has_selling_stock',0)
        
        # Price range filter
        if min_price != 0:
            query = query.filter(price__gte=min_price)
        if max_price != 0:
            query = query.filter(price__lte=max_price)

        #Check for product avaiability
        if has_selling_stock == '1':
            query = query.filter(quantity__gte=1)
        
        #Order based filter
        if order != 'default':
            if order == 'popular':
                query = query.order_by('-rate',)
            elif order == 'price_ascending':
                query = query.order_by('price')
            elif order == 'price_descending':
                query = query.order_by('-price')
   
        
        return query.select_related('category')
    

