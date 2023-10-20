from .models import State
from rest_framework.generics import (
    ListAPIView,
)
from .serializers import StateCityListSerilizer


class LocationListAPIView(ListAPIView):
    """
    Get state and cities associated with them.
    """

    serializer_class = StateCityListSerilizer

    def get_queryset(self):
        return State.objects.all()

# class AddressViewSet(ModelViewSet):
#     """
#     View set for retrieve, update, delete and create address.
#     """

#     permission_classes = [IsAuthenticated]
#     serializer_class = AddressSerializer

#     def get_queryset(self):
#         return Address.objects.filter(user=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)