from rest_framework.pagination import PageNumberPagination

class UserCommentListPagination(PageNumberPagination):
    page_size_query_param = "page_size"
    max_page_size = 100
    page_size = 5
