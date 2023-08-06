from django.db.models import Q
from modules.utility.utils.cache import delete_data_from_cache


def filter_products_by_price(queryset, min_price, max_price):
    if min_price > 0:
        queryset &= Q(price__gte=min_price)
    if max_price > 0:
        queryset &= Q(price__lte=max_price)
    return queryset


def filter_products_by_availability(queryset, has_selling_stock):
    if has_selling_stock.lower() == "true":
        queryset &= Q(quantity__gte=1)
    return queryset


def sort_products(queryset, sort):
    SORT_QUERIES = {
        "popular": "-rate",
        "cheapest": "price",
        "most_expensive": "-price",
        "newest": "-created_at",
        "bestselling": "-sold",
        "most_viewed": "-views",
    }
    sort_order = SORT_QUERIES.get(sort, "-created_at")
    return queryset.order_by(sort_order)


SORT_CHOICES = ("newest", "bestselling", "most_viewed")


def is_sort_invalid(sort_method):
    return sort_method not in SORT_CHOICES


def delete_all_product_list_caches():
    for sort_method in SORT_CHOICES:
        delete_data_from_cache(f"product_list_{sort_method}")
