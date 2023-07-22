from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import *
from .models import ShoppingSession
from django.http import Http404
from rest_framework.viewsets import ModelViewSet
from django.db import transaction


class CreateCartItems(generics.CreateAPIView):
    """
    View for creating cart items.
    """

    serializer_class = CartItemCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = serializer.validated_data["product"]
        quantity = serializer.validated_data["quantity"]
        shopping_session, _ = ShoppingSession.objects.get_or_create(
            user=self.request.user
        )

        CartItem.objects.update_or_create(
            product=product, session=shopping_session, defaults={
                "quantity": quantity}
        )
        shopping_session.update_total()
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
        instance = self.get_cart_item_by_product_id(kwargs.get("pk"))
        serilizer = self.serializer_class(instance=instance)
        return Response(serilizer.data)

    def destroy(self, request, *args, **kwargs):
        cart_item = self.get_cart_item_by_product_id(kwargs.get("pk"))
        shopping_session = cart_item.session
        self.perform_destroy(cart_item)
        shopping_session.update_total()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_cart_item_by_product_id(self, id):
        try:
            cart_item = CartItem.objects.get(
                product__id=id, session__user=self.request.user
            )
        except CartItem.DoesNotExist:
            raise Http404()

        return cart_item


class CartItemsList(generics.ListAPIView):
    """
    Get session and cart items associated with it.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = CartItemsListSerializer

    def get_queryset(self):
        session = ShoppingSession.objects.filter(user=self.request.user)
        return session


class DeleteAllCartItems(generics.DestroyAPIView):
    """
    Delete all cart items associated with the authenticated user.
    """

    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        CartItem.objects.filter(session__user=self.request.user).delete()
        ShoppingSession.objects.get(user=request.user).update_total()
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

    def perform_create(self, serializer):
        order_items_data = self.request.data.get("order_items")

        with transaction.atomic():
            payment_data = serializer.validated_data["payment"]
            payment = Payment.objects.create(
                amount=serializer.validated_data["total"],
                payment_method=payment_data["payment_method"]
            )

            order = serializer.save(payment=payment, user=self.request.user)

            order_item_serializer = OrderItemSerializer(
                data=order_items_data, many=True)
            order_item_serializer.is_valid(raise_exception=True)

            order_items = [
                OrderItem(
                    order=order,
                    product=item["product"],
                    quantity=item["quantity"]
                )
                for item in order_item_serializer.validated_data
            ]
            OrderItem.objects.bulk_create(order_items)



class RUDOrderView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RUDOrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(id=self.kwargs["pk"], user=self.request.user)


class RUDOrderItemView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OrderItem.objects.filter(id=self.kwargs['pk'])


class RUDPaymentView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(id=self.kwargs['pk'])
