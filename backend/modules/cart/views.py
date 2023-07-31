from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    RetrieveDestroyAPIView,
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    DestroyAPIView,
)
from .serializers import *
from .models import ShoppingSession
from .helpers import *
from modules.utility.permissions import IsSuperuserOrObjectOwner
from modules.utility.mixins import SingleFieldUrlGetObjectMixin


class CreateCartItems(CreateAPIView):
    """
    View for creating cart items.
    """

    serializer_class = CartItemCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        shopping_session = ShoppingSession.objects.get_or_create_shopping_session(
            request.user
        )
        CartItem.objects.create_or_update_cart_item(
            shopping_session, **serializer.validated_data
        )

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class RUDCartItem(RetrieveDestroyAPIView):
    """
    View for retrieve and delete cart item.
    """

    serializer_class = RDCartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        productId = self.kwargs.get("pk")
        return get_object_or_404(CartItem, product__id=productId, session__user=user)

    def destroy(self, request, *args, **kwargs):
        cart_item = self.get_object()
        CartItem.objects.delete_one_cart_item(cart_item)
        return Response(status=status.HTTP_204_NO_CONTENT)


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
        CartItem.objects.delete_all_user_cart_items(request.user)
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
            return invalid_order_response()

        order_item_serializer = OrderItemSerializer(data=order_items_data, many=True)
        order_item_serializer.is_valid(raise_exception=True)

        order_data, payment_data = serialize_order_and_payment_data(
            serializer.validated_data
        )

        order = Order.objects.create_order_with_payment_and_items(
            request.user, order_data, payment_data, order_item_serializer.validated_data
        )

        return success_order_created_response(order)


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
