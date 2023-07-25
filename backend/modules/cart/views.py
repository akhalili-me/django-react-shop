from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import *
from .models import ShoppingSession
from .helpers import *


class CreateCartItems(generics.CreateAPIView):
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


class RDCartItems(generics.RetrieveDestroyAPIView):
    """
    View for retrieve and delete cart item.
    """

    serializer_class = RDCartItemSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        cart_item_object = CartItem.objects.get_cart_item_by_product_id(
            kwargs.get("pk"), request.user
        )
        serilizer = self.serializer_class(instance=cart_item_object)
        return Response(serilizer.data)

    def destroy(self, request, *args, **kwargs):
        CartItem.objects.delete_one_cart_item(kwargs.get("pk"), request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartItemsList(generics.ListAPIView):
    """
    Get session and cart items associated with it.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = CartItemsListSerializer

    def get_queryset(self):
        return ShoppingSession.objects.filter(user=self.request.user)


class DeleteAllCartItems(generics.DestroyAPIView):
    """
    Delete all cart items associated with the authenticated user.
    """

    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        CartItem.objects.delete_all_user_cart_items(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class StateCityList(generics.ListAPIView):
    """
    Get state and cities associated with them.
    """

    serializer_class = StateCityListSerilizer

    def get_queryset(self):
        return State.objects.all()


class ListUserOrdersView(generics.ListAPIView):
    serializer_class = ListOrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by("-created_at")


class CreateOrdersView(generics.CreateAPIView):
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


class RUDOrderView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RUDOrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(id=self.kwargs["pk"], user=self.request.user)


class RUDOrderItemView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OrderItem.objects.filter(id=self.kwargs["pk"])


class RUDPaymentView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(id=self.kwargs["pk"])
