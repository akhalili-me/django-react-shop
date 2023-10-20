from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Payment


@receiver(post_save, sender=Payment)
def update_product_quantity_on_payment_success(sender, instance, **kwargs):
    if instance.status == "paid":
        # print(instance.status)
        order = instance.order

        order_items = order.order_items.all()

        for order_item in order_items:
            order_item.product.quantity -= order_item.quantity
            order_item.product.save()
