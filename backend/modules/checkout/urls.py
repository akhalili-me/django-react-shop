from django.urls import path
from .views import (
    PaymentRetrieveUpdateDestroyAPIView,
)

app_name = "checkout"

urlpatterns = [
    path(
        "payment/<int:order_id>",
        PaymentRetrieveUpdateDestroyAPIView.as_view(),
        name="payment-retrieve-update-destroy",
    ),
]