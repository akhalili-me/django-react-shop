from rest_framework import viewsets,permissions
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status

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


class ProductCommentsListView(generics.ListAPIView):
    """
    ViewSet for listing product comments.
    """
    serializer_class = ProductCommentListSerializer
    permission_classes = []
    
    def get_queryset(self):
        """
        Return the comments associated with a particular product id.
        """
        product_id = self.kwargs['product_id']
        return Comment.objects.filter(product_id=product_id).order_by('-created_at')
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
class ProductCommentsCreateView(generics.CreateAPIView):
    """
    ViewSet for creating product comments.
    """

    serializer_class = ProductCommentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self,request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(product_id=kwargs['product_id'], author=self.request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(status=status.HTTP_201_CREATED,headers=headers)


class FilterPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_size = 9


class ProductsFilterListView(generics.ListAPIView):
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
        min_price = int(self.request.query_params.get('min',0))
        max_price = int(self.request.query_params.get('max',0))
        has_selling_stock = self.request.query_params.get('has_selling_stock','false')

        filter_queries = Q()
        # Price range filter
        if min_price > 0:
            filter_queries &= Q(price__gte=min_price)
        if max_price > 0:
            filter_queries &= Q(price__lte=max_price)

        #Check for product avaiability
        if has_selling_stock == 'true':
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
    

