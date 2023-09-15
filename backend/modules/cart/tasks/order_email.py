from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


@shared_task
def send_order_confirm_email(email,order):
    subject = "Thank you for your order!"
    html_msg = render_to_string('emails/order_email.html',{'order': order})
    plain_message = strip_tags(html_msg)
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email,]

    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_msg)
