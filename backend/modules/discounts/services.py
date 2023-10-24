from django.utils import timezone
from .api_exceptions import DiscountInvalidException
from django.shortcuts import get_object_or_404


class DiscountService:
    @staticmethod
    def apply_discount(discount, total_price):
        if discount.type == "fixed":
            final_price = total_price - discount.value
        else:
            discount_amount = (discount.value * total_price) / 100
            final_price = total_price - discount_amount
        return round(final_price, 2)

    @staticmethod
    def calculate_discount_amount(discount, total_price):
        if discount.type == "fixed":
            return discount.value
        else:
            return (discount.value * total_price) / 100

    @staticmethod
    def validate_discount(code, user):
        from .models import Discount

        discount = get_object_or_404(Discount, code=code)
        DiscountService._verify_discount_active_status(discount)
        DiscountService._verify_discount_user_validity(discount, user)
        DiscountService._verify_discount_not_previously_used(discount, user)
        return discount

    @staticmethod
    def _verify_discount_active_status(discount):
        if discount.is_active == False or discount.expire_at < timezone.now():
            raise DiscountInvalidException()

    @staticmethod
    def _verify_discount_user_validity(discount, user):
        if discount.user and discount.user != user:
            raise DiscountInvalidException()

    @staticmethod
    def _verify_discount_not_previously_used(discount, user):
        from .models import DiscountUsage

        is_discount_used = DiscountUsage.objects.filter(
            discount=discount, user=user
        ).exists()

        if is_discount_used:
            raise DiscountInvalidException()
