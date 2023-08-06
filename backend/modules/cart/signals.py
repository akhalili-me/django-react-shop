from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import CartItem


@receiver(post_save, sender=CartItem)
@receiver(post_delete, sender=CartItem)
def update_session_total(sender, instance, **kwargs):
    instance.session.update_total()
