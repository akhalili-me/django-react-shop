from .models import OrderItem, Order
from modules.checkout.models import Payment
from modules.discounts.models import Discount
from django.db import transaction
from modules.discounts.services import DiscountService
from modules.utility.loading import get_model

UserAddress = get_model("shipment", "UserAddress")
BillingAddress = get_model("shipment", "BillingAddress")


class OrderService:
    @staticmethod
    def process_order_and_payment(user, data):
        with transaction.atomic():
            billing_address = BillingAddress.objects.create_bill_addr_from_user_addr(
                data["address"]
            )
            order_kwargs = {
                "user": user,
                "billing_address": billing_address,
                "shipping_price": data["shipping_price"],
                "total": data["total"],
            }
            order = Order.objects.create(**order_kwargs)

            discount_code = getattr(data, "discount", None)
            if discount_code:
                discount = Discount.objects.get(code=discount_code)
                payment_amount = DiscountService.apply_discount(discount, order.total)
            else:
                payment_amount = order.total

            payment_kwargs = {
                "amount": payment_amount,
                "method": data["payment_method"],
                "order": order,
                "is_main_payment": True,
            }
            Payment.objects.create(**payment_kwargs)

            OrderItem.objects.create_order_items(order, data["order_items"])
            return order
