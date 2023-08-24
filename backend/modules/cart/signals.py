from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import CartItem, OrderItem, Payment


@receiver(post_save, sender=CartItem)
@receiver(post_delete, sender=CartItem)
def update_session_total(sender, instance, **kwargs):
    instance.session.update_total()

@receiver(post_save, sender=Payment)
def update_product_quantity(sender, instance, **kwargs):
    if instance.status == "paid":
        order = instance.order

        order_items = order.order_items.all()

        for order_item in order_items:
            order_item.product.quantity -= order_item.quantity
            order_item.product.save()
