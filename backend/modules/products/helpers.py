from django.core.cache import cache


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
