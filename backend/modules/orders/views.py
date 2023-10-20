from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from modules.utility.permissions import IsSuperUserOrObjectOwner
from .serializers import (
    OrdersListSerializer,
    OrderCreateSerializer,
    OrderDetailsSerializer,
    OrderItemSerializer,
)
from .models import Order, OrderItem


class ListCreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by("-created_at")
        serializer = OrdersListSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serilizer = OrderCreateSerializer(data=request.data)
        serilizer.is_valid(raise_exception=True)
        order = Order.objects.create_order_with_payment_and_items(
            request.user, serilizer.validated_data
        )
        response_data = OrderDetailsSerializer(order).data
        # send_order_confirm_email.delay(self.request.user.email, response_data)
        return Response(response_data, status=status.HTTP_201_CREATED)


class OrderRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = OrderDetailsSerializer
    permission_classes = [IsSuperUserOrObjectOwner]
    queryset = Order.objects.all()


class OrderItemRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [IsSuperUserOrObjectOwner]
    queryset = OrderItem.objects.all()
    user_field = "order.user"
