from rest_framework import status
from rest_framework.exceptions import APIException


class CommentAlreadyLikedException(APIException):
    default_detail = "Comment is already liked by you"
    status_code = status.HTTP_400_BAD_REQUEST


class SortMethodInvalidException(APIException):
    default_detail = "Sort method is not valid."
    status_code = status.HTTP_400_BAD_REQUEST
