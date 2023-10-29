from .models import OrderItem, Order
from modules.checkout.models import Payment
from modules.discounts.models import Discount
from django.db import transaction
from modules.discounts.services import DiscountService


class OrderService:
    @staticmethod
    def process_order_and_payment(user, data):
        with transaction.atomic():
            order = Order.objects.create(
                user=user,
                address=data["address"],
                shipping_price=data["shipping_price"],
                total=data["total"],
            )

            discount_code = getattr(data, "discount", None)
            if discount_code:
                discount = Discount.objects.get(code=discount_code)
                payment_amount = DiscountService.apply_discount(discount, order.total)
            else:
                payment_amount = order.total

            Payment.objects.create(
                amount=payment_amount,
                method=data["payment_method"],
                order=order,
                is_main_payment=True,
            )
            OrderItem.objects.create_order_items(order, data["order_items"])

            return order
