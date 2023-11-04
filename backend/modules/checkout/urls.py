from django.urls import path
from .views import (
    PaymentRetrieveUpdateDestroyAPIView,
)

app_name = "checkout"

urlpatterns = [
    path(
        "payment/<uuid:uuid>",
        PaymentRetrieveUpdateDestroyAPIView.as_view(),
        name="payment-detail",
    ),
]
