from django.urls import path,include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')
router.register('',ProductViewSet,basename='products')
router.register(r'(?P<product_id>\d+)/images', ProductImageViewSet, basename='product_images')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:product_id>/comments',ProductCommentsCreateListView.as_view()),
    path('search/<int:pk>', ProductsFilterListView.as_view()),
]