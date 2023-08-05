from rest_framework.exceptions import APIException
from rest_framework import status


class OrderItemsEmptyException(APIException):
    default_detail = "Order items cannot be empty."
    status_code = status.HTTP_400_BAD_REQUEST
