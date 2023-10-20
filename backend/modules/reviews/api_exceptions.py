from rest_framework import status
from rest_framework.exceptions import APIException


class CommentAlreadyLikedException(APIException):
    default_detail = "Comment is already liked by current user."
    status_code = status.HTTP_400_BAD_REQUEST


class ReportAlreadyTakenException(APIException):
    default_detail = "Report has already been taken by current user."
    status_code = status.HTTP_400_BAD_REQUEST


class MaxDailyReportReachedException(APIException):
    default_detail = "You have reached the daily limit of reports."
    status_code = status.HTTP_403_FORBIDDEN
