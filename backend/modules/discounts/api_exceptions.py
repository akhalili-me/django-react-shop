from rest_framework import status
from rest_framework.exceptions import APIException


class DiscountInvalidException(APIException):
    default_detail = "Discount code is either invalid or already used."
    status_code = status.HTTP_400_BAD_REQUEST
