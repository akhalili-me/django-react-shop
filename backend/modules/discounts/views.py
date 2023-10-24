from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Discount
from modules.cart.models import ShoppingSession
from .serializers import DiscountSerializer
from rest_framework.response import Response
from rest_framework import status
from .services import DiscountService


class DiscountCreateView(CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = DiscountSerializer


class DiscountRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = DiscountSerializer
    queryset = Discount.objects.all()


class ApplyDiscountView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        discount = DiscountService.validate_discount(request.data["code"], request.user)
        shopping_session = ShoppingSession.objects.get(user=request.user)
        final_price = DiscountService.apply_discount(discount, shopping_session.total)
        return Response(final_price, status=status.HTTP_200_OK)
