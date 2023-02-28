from rest_framework import viewsets,permissions
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *


class ProductViewSet(ModelViewSet):
    """
    ViewSet for viewing and editing the products.
    """
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Product.objects.all()


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
    
    

