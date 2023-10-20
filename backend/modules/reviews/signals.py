from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Comment
from modules.products.helpers import delete_all_product_list_caches

@receiver(post_save, sender=Comment)
@receiver(post_delete, sender=Comment)
def update_product_rate_and_clear_product_cache(sender, instance, **kwargs):
    instance.product.update_rate()
    delete_all_product_list_caches()


