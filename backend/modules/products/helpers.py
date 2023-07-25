from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q


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
        "default": "-created_at",
        "popular": "-rate",
        "cheapest": "price",
        "most_expensive": "-price",
        "newest": "-created_at",
        "bestselling": "-sold",
    }
    sort_order = SORT_QUERIES.get(sort, "-created_at")
    return queryset.order_by(sort_order)


def comment_already_liked_response():
    return Response(
        {"detail": "This comment is already liked by this user."},
        status=status.HTTP_400_BAD_REQUEST,
    )