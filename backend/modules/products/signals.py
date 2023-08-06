from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Comment


@receiver(post_save, sender=Comment)
@receiver(post_delete, sender=Comment)
def update_product_rate(sender, instance, **kwargs):
    instance.product.update_rate()
