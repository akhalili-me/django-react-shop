from django.db.models import Q


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