from django.db import models


class OrderItemManager(models.Manager):
    def create_order_items(self, order, order_items_data):
        from .models import OrderItem

        order_items = [
            OrderItem(order=order, product=item["product"], quantity=item["quantity"])
            for item in order_items_data
        ]
        self.bulk_create(order_items)
