from rest_framework.pagination import PageNumberPagination

class CommentsPagination(PageNumberPagination):
    page_size_query_param = "comment_size"
    max_page_size = 100
    page_size = 6

