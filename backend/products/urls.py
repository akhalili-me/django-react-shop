from django.urls import path,include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')
router.register('',ProductViewSet,basename='products')
router.register(r'(?P<product_id>\d+)/comments', CommentViewSet, basename='comments')
router.register(r'(?P<product_id>\d+)/images', ProductImageViewSet, basename='product_images')
# router.register(r'search/(?P<pk\d+)',,basename='search')

urlpatterns = [
    path('', include(router.urls)),
    path('search/<int:pk>', ProductsFilter.as_view()),
]