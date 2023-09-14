from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from time import sleep

@shared_task
def send_order_info_email(email,order):
    subject = "Thank you for your order!"
    message = f"""
    Your order has been successfully processed.
    Order ID = {order["id"]}
    Payment = {order["payment"]}
    Items = {order["order_items"]}
    Shipping price = {order["shipping_price"]}
    Address = {order["full_address"]}
    """
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ["amir.khalily487@gmail.com",]

    send_mail(subject, message, from_email, recipient_list)
