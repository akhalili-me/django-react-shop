from rest_framework.response import Response
from rest_framework import status


def invalid_order_response():
    return Response(
        {"detail": "Order items cannot be empty."}, status=status.HTTP_400_BAD_REQUEST
    )


def success_order_created_response(order):
    response_data = {
        "order_id": order.id,
        "payment_id": order.payment.id,
        "message": "Order created successfully!",
    }

    return Response(response_data, status=status.HTTP_201_CREATED)


def serialize_order_and_payment_data(data):
    payment_data = {
        "amount": data["total"],
        "payment_method": data["payment"]["payment_method"],
    }
    order_data = {
        "address": data["address"],
        "shipping_price": data["shipping_price"],
        "total": data["total"],
    }
    return order_data, payment_data
