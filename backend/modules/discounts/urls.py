from django.urls import path
from .views import (
    DiscountCreateView,
    DiscountRetrieveUpdateDestroyView,
    ApplyDiscountView,
)

app_name = "discounts"

urlpatterns = [
    path("", DiscountCreateView.as_view(), name="discount-create"),
    path(
        "<int:pk>",
        DiscountRetrieveUpdateDestroyView.as_view(),
        name="discount-retrieve-update-delete",
    ),
    path("apply", ApplyDiscountView.as_view(), name="discount-apply"),
]
