from django.db import models, transaction
from django.shortcuts import get_object_or_404
from django.db.models import F


class OrderManager(models.Manager):
    def create_order_with_payment_and_items(
        self, user, order_data, payment_data, order_items_data
    ):
        from .models import Payment, OrderItem

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
            OrderItem.objects.create_order_items(order, order_items_data)

            return order


class OrderItemManager(models.Manager):
    def create_order_items(self, order, order_items_data):
        from .models import OrderItem
        from modules.products.models import Product

        order_items = []
        products = []

        for order_item in order_items_data:
            # order items objects array
            order_item_instance = OrderItem(
                order=order,
                product=order_item["product"],
                quantity=order_item["quantity"],
            )
            order_items.append(order_item_instance)

            # product objects array
            product_instance = Product(pk=order_item_instance.product.id)
            product_instance.quantity = F("quantity") - order_item_instance.quantity
            product_instance.sold = F("sold") + order_item_instance.quantity
            products.append(product_instance)

        with transaction.atomic():
            OrderItem.objects.bulk_create(order_items)
            Product.objects.bulk_update(products, ["quantity", "sold"])


class CartItemManager(models.Manager):
    def create_or_update_cart_item(self, shopping_session, **kwargs):
        from .models import CartItem

        CartItem.objects.update_or_create(
            product=kwargs["product"],
            session=shopping_session,
            defaults={"quantity": kwargs["quantity"]},
        )

        shopping_session.update_total()

    def delete_one_cart_item(self, cart_item):
        with transaction.atomic():
            shopping_session = cart_item.session
            cart_item.delete()
            shopping_session.update_total()

    def delete_all_user_cart_items(self, user):
        from .models import CartItem, ShoppingSession

        shopping_session = get_object_or_404(ShoppingSession, user=user)
        CartItem.objects.filter(session=shopping_session).delete()
        shopping_session.update_total()


class ShoppingSessionManager(models.Manager):
    def get_or_create_shopping_session(self, user):
        from .models import ShoppingSession

        shopping_session, _ = ShoppingSession.objects.get_or_create(user=user)
        return shopping_session
