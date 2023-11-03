from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.core.cache import cache
from .models import Category, Product
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@receiver(post_save, sender=Category)
@receiver(post_delete, sender=Category)
def clear_category_cache(sender, instance, **kwargs):
    cache.delete("category_list")


@receiver(pre_save, sender=Product)
def handle_price_update(sender, instance, **kwargs):
    if instance._state.adding:
        return

    original_price = float(sender.objects.get(pk=instance.pk).price)
    new_price = float(instance.price)
    if new_price != original_price:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "product_updates",
            {
                "type": "price_update",
                "content": {"product_id": instance.id, "new_price": new_price},
            },
        )
