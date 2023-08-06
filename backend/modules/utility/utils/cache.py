from django.core.cache import cache


def get_data_from_cache(cache_key):
    data = cache.get(cache_key)
    return data


def delete_data_from_cache(cache_key):
    cache.delete(cache_key)
