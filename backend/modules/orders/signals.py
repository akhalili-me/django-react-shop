from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from modules.cart.models import ShoppingSession


@receiver(post_save, sender=Order)
def update_session_total(sender, instance, **kwargs):
    shopping_session = ShoppingSession.objects.get(user=instance.user)
    shopping_session.clear_session()
