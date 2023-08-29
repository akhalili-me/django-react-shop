from rest_framework.response import Response
from rest_framework import status


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
