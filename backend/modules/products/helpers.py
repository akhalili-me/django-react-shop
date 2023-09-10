from django.db.models import Q
from django.core.cache import cache


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


def get_sort_order(sort):
    SORT_QUERIES = {
        "popular": "-rate",
        "cheapest": "price",
        "most_expensive": "-price",
        "bestselling": "-sold",
        "most_viewed": "-views",
    }
    sort_order = SORT_QUERIES.get(sort, "-created_at")

    return sort_order


SORT_CHOICES = ("newest", "bestselling", "most_viewed")


def is_sort_invalid(sort_method):
    return sort_method not in SORT_CHOICES


def delete_all_product_list_caches():
    for sort_method in SORT_CHOICES:
        cache.delete(f"product_list_{sort_method}")
