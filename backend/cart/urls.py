from django.urls import path,include
from rest_framework import routers
from .views import *


urlpatterns = [
    path('', CartItemsList.as_view()),
    path('create', CreateCartItems.as_view()),
    path('<int:pk>/', RUDCartItems.as_view()),
]