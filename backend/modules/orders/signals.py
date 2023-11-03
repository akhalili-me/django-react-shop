from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from modules.cart.models import ShoppingSession


@receiver(post_save, sender=Order)
def clear_session_after_order_save(sender, instance, **kwargs):
    shopping_session = ShoppingSession.objects.get(user=instance.user)
    shopping_session.clear_session()
