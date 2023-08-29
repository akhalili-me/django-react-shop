from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    RetrieveDestroyAPIView,
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    DestroyAPIView,
)
from modules.utility.permissions import IsSuperuserOrObjectOwner
from modules.utility.mixins import SingleFieldUrlGetObjectMixin
from .serializers import (
    CartItemCreateSerializer,
    RDCartItemSerializer,
    CartItemsListSerializer,
    StateCityListSerilizer,
    PaymentSerializer,
    OrderItemSerializer,
    RUDOrderSerializer,
    CreateOrderSerializer,
    ListOrderSerializer,
)
from .helpers import serialize_order_and_payment_data, success_order_created_response
from .models import ShoppingSession, CartItem, State, Order, OrderItem, Payment
from .api_exceptions import OrderItemsEmptyException


class CreateCartItems(CreateAPIView):
    """
    View for creating cart items.
    """

    serializer_class = CartItemCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        shopping_session, _ = ShoppingSession.objects.get_or_create(user=request.user)
        CartItem.objects.update_or_create(
            product=serializer.validated_data["product"],
            session=shopping_session,
            defaults={"quantity": serializer.validated_data["quantity"]},
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RDCartItem(RetrieveDestroyAPIView):
    """
    View for retrieve and delete cart item.
    """

    serializer_class = RDCartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        productId = self.kwargs.get("pk")
        return get_object_or_404(CartItem, product__id=productId, session__user=user)


class CartItemsList(RetrieveAPIView):
    """
    Get session and cart items associated with it.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = CartItemsListSerializer

    def get_object(self):
        return get_object_or_404(ShoppingSession, user=self.request.user)


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


class ListUserOrdersView(ListAPIView):
    serializer_class = ListOrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by("-created_at")


class CreateOrdersView(CreateAPIView):
    serializer_class = CreateOrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order_items_data = request.data.get("order_items")

        if not order_items_data or len(order_items_data) == 0:
            raise OrderItemsEmptyException()

        order_item_serializer = OrderItemSerializer(data=order_items_data, many=True)
        order_item_serializer.is_valid(raise_exception=True)

        order_data, payment_data = serialize_order_and_payment_data(
            serializer.validated_data
        )

        order = Order.objects.create_order_with_payment_and_items(
            request.user, order_data, payment_data, order_item_serializer.validated_data
        )
        return Response(RUDOrderSerializer(order).data, status=status.HTTP_201_CREATED)


class RUDOrderView(SingleFieldUrlGetObjectMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = RUDOrderSerializer
    permission_classes = [IsSuperuserOrObjectOwner]
    model = Order


class RUDOrderItemView(SingleFieldUrlGetObjectMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [IsSuperuserOrObjectOwner]
    model = OrderItem


class RUDPaymentView(SingleFieldUrlGetObjectMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsSuperuserOrObjectOwner]
    model = Payment
    filter_field = "order__id"
