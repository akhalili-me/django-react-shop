from rest_framework.pagination import PageNumberPagination


class ProductListPagination(PageNumberPagination):
    page_size_query_param = "page_size"
    max_page_size = 100
    page_size = 6
