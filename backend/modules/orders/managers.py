from django.db import models, transaction
from modules.discounts.services import DiscountService


class OrderManager(models.Manager):
    def create_order_with_payment_and_items(self, user, data):
        from .models import OrderItem
        from modules.checkout.models import Payment
        from modules.discounts.models import Discount

        with transaction.atomic():
            order = self.create(
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


class OrderItemManager(models.Manager):
    def create_order_items(self, order, order_items_data):
        from .models import OrderItem

        order_items = [
            OrderItem(order=order, product=item["product"], quantity=item["quantity"])
            for item in order_items_data
        ]
        self.bulk_create(order_items)
