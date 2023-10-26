from .services import DiscountService
from django.db import models


class DiscountUsageManager(models.Manager):
    def check_and_create_discount_usage(self, user, discount, order):
        from .models import DiscountUsage, Discount

        if discount:
            discount = Discount.objects.get(code=discount)
            discount_amount = DiscountService.calculate_discount_amount(
                discount, order.total
            )

            return DiscountUsage.objects.create(
                order=order,
                discount=discount,
                user=user,
                amount=discount_amount,
            )
