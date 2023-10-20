from rest_framework.generics import RetrieveUpdateDestroyAPIView
from modules.utility.permissions import IsSuperUserOrObjectOwner
from .serializers import (
    PaymentSerializer,
)
from .models import Payment
from django.shortcuts import get_object_or_404


class PaymentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsSuperUserOrObjectOwner]
    user_field = "order.user"

    def get_object(self):
        payment = get_object_or_404(Payment, order__id=self.kwargs["order_id"])
        self.check_object_permissions(self.request, payment)
        return payment
