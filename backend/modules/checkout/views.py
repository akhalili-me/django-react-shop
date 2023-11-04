from rest_framework.generics import RetrieveUpdateDestroyAPIView
from modules.utility.permissions import IsSuperUserOrObjectOwner
from .serializers import (
    PaymentSerializer,
)
from .models import Payment


class PaymentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsSuperUserOrObjectOwner]
    user_field = "order.user"
    queryset = Payment.objects.all()
    lookup_field = "uuid"
