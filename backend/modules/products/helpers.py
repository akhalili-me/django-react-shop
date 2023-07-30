from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.core.cache import cache

def filter_products_by_price(queryset, min_price, max_price):
    filter_queries = Q()
    if min_price > 0:
        filter_queries &= Q(price__gte=min_price)
    if max_price > 0:
        filter_queries &= Q(price__lte=max_price)
    return queryset.filter(filter_queries)


def filter_products_by_availability(queryset, has_selling_stock):
    if has_selling_stock.lower() == "true":
        return queryset.filter(quantity__gte=1)
    return queryset


def sort_products(queryset, sort):
    SORT_QUERIES = {
        "popular": "-rate",
        "cheapest": "price",
        "most_expensive": "-price",
        "newest": "-created_at",
        "bestselling": "-sold",
        "most_viewed": "-views"
    }
    sort_order = SORT_QUERIES.get(sort, "-created_at")
    return queryset.order_by(sort_order)


def comment_already_liked_response():
    return Response(
        {"detail": "This comment is already liked by this user."},
        status=status.HTTP_400_BAD_REQUEST,
    )


def get_data_from_cache(cache_key):
    data = cache.get(cache_key)
    return data


def is_sort_invalid(sort_method):
    SORT_CHOICES = ("newest", "bestselling", "most_viewed")
    return sort_method not in SORT_CHOICES

def sort_invalid_response():
    return Response(
        {"detail": "Sort method is not valid."},
        status=status.HTTP_400_BAD_REQUEST,
    )