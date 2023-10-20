from django.db import models, transaction
from django.shortcuts import get_object_or_404
from django.db.models import F


class OrderManager(models.Manager):
    def create_order_with_payment_and_items(self, user, data):
        from .models import Payment, OrderItem

        with transaction.atomic():
            # Create the payment
            payment = Payment.objects.create(
                amount=data["total"], payment_method=data["payment_method"]
            )

            # Create the order
            order = self.create(
                user=user,
                payment=payment,
                address=data["address"],
                shipping_price=data["shipping_price"],
                total=data["total"],
            )

            # Create the order items
            OrderItem.objects.create_order_items(order, data["order_items"])

            return order


class OrderItemManager(models.Manager):
    def create_order_items(self, order, order_items_data):
        from .models import OrderItem

        order_items = [
            OrderItem(order=order, product=item["product"], quantity=item["quantity"])
            for item in order_items_data
        ]
        self.bulk_create(order_items)

