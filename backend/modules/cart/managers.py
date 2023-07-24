from django.db import models, transaction
from django.shortcuts import get_object_or_404


class OrderManager(models.Manager):
    def create_order_with_payment_and_items(
        self, user, order_data, payment_data, order_items_data
    ):
        from .models import Payment

        with transaction.atomic():
            # Create the payment
            payment = Payment.objects.create(**payment_data)

            # Create the order
            order = self.create(
                user=user,
                payment=payment,
                **order_data,
            )

            # Create the order items
            self.create_order_items(order, order_items_data)

            return order

    def create_order_items(self, order, order_items_data):
        from .models import OrderItem

        order_items = [
            OrderItem(order=order, product=item["product"], quantity=item["quantity"])
            for item in order_items_data
        ]
        OrderItem.objects.bulk_create(order_items)


class CartItemManager(models.Manager):
    def create_or_update_cart_item(self, shopping_session, **kwargs):
        from .models import CartItem

        CartItem.objects.update_or_create(
            product=kwargs["product"],
            session=shopping_session,
            defaults={"quantity": kwargs["quantity"]},
        )

        shopping_session.update_total()

    def delete_one_cart_item(self, user, product_id):
        with transaction.atomic():
            cart_item = self.get_cart_item_by_product_id(product_id, user)
            shopping_session = cart_item.session
            cart_item.delete()
            shopping_session.update_total()

    def delete_all_user_cart_items(self, user):
        from .models import CartItem, ShoppingSession

        shopping_session = get_object_or_404(ShoppingSession, user=user)
        CartItem.objects.filter(session__user=user).delete()
        shopping_session.update_total()

    def get_cart_item_by_product_id(self, product_id, user):
        from .models import CartItem

        return get_object_or_404(CartItem, product__id=product_id, session__user=user)


class ShoppingSessionManager(models.Manager):
    def get_or_create_shopping_session(self, user):
        from .models import ShoppingSession

        shopping_session, _ = ShoppingSession.objects.get_or_create(user=user)
        return shopping_session
