from rest_framework.response import Response
from rest_framework import status

def invalid_order_response():
    return Response(
        {"detail": "Order items cannot be empty."}, status=status.HTTP_400_BAD_REQUEST
    )

