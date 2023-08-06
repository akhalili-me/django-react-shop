from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from modules.utility.utils.cache import delete_data_from_cache
from .models import Comment, Category
from .helpers import delete_all_product_list_caches


@receiver(post_save, sender=Comment)
@receiver(post_delete, sender=Comment)
def update_product_rate_and_clear_product_cache(sender, instance, **kwargs):
    instance.product.update_rate()
    delete_all_product_list_caches()


@receiver(post_save, sender=Category)
@receiver(post_delete, sender=Category)
def clear_category_cache(sender, instance, **kwargs):
    delete_data_from_cache("category_list")
