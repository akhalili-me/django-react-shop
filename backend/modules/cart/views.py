from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
    DestroyAPIView,
)
from modules.utility.permissions import IsSuperUserOrObjectOwner
from .serializers import (
    SessionAndCartItemsListSerializer,
    CartItemCreateSerializer,
    StateCityListSerilizer,
    PaymentSerializer,
    OrderItemSerializer,
    OrderDetailsSerializer,
    OrdersListSerializer,
    OrderCreateSerializer,
)
from .models import ShoppingSession, CartItem, State, Order, OrderItem, Payment
from .tasks.order_email import send_order_confirm_email


class ListCreateUpdateCartItem(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        shopping_session, _ = ShoppingSession.objects.get_or_create(user=request.user)
        serializer = SessionAndCartItemsListSerializer(shopping_session)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CartItemCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        shopping_session, _ = ShoppingSession.objects.get_or_create(user=request.user)
        CartItem.objects.update_or_create(
            product=serializer.validated_data["product"],
            session=shopping_session,
            defaults={"quantity": serializer.validated_data["quantity"]},
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DestroyCartItem(DestroyAPIView):
    permission_classes = [IsSuperUserOrObjectOwner]
    queryset = CartItem.objects.all()
    user_field = "session.user"
    lookup_field = "product__id"
    lookup_url_kwarg = "product_id"


class DeleteAllCartItems(DestroyAPIView):
    """
    Delete all cart items associated with the authenticated user.
    """

    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        shopping_session = get_object_or_404(ShoppingSession, user=request.user)
        CartItem.objects.filter(session=shopping_session).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StateCityList(ListAPIView):
    """
    Get state and cities associated with them.
    """

    serializer_class = StateCityListSerilizer

    def get_queryset(self):
        return State.objects.all()


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
        send_order_confirm_email.delay(self.request.user.email, response_data)
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


class PaymentRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsSuperUserOrObjectOwner]
    queryset = Payment.objects.all()
    user_field = "order.user"
    lookup_field = "order__id"
    lookup_url_kwarg = "order_id"
