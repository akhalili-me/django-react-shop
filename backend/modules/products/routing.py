from django.urls import path

from .consumers import ProductConsumer

websocket_urlpatterns = [
    path("ws/product_update/", ProductConsumer.as_asgi()),
]