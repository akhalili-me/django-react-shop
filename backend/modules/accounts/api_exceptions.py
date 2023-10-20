from rest_framework import status
from rest_framework.exceptions import APIException


class UserBannedForThisActionException(APIException):
    def __init__(self, ban_type):
        self.detail = f"User is banned for {ban_type} actions."

    status_code = status.HTTP_403_FORBIDDEN
