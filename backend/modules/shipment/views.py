from .models import State, Address
from rest_framework.generics import (
    ListCreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from .serializers import StateCityListSerilizer, AddressSerializer
from modules.utility.permissions import IsSuperUserOrObjectOwner


class LocationListView(ListAPIView):
    """
    Get state and cities associated with them.
    """

    serializer_class = StateCityListSerilizer

    def get_queryset(self):
        return State.objects.all()

class UserAddressListView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AddressRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsSuperUserOrObjectOwner]
    serializer_class = AddressSerializer
    queryset = Address.objects.all()
