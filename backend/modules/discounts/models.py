from modules.utility.models import TimeStampedModel
from django.db import models
from .managers import DiscountUsageManager
from modules.orders.models import Order
from django.core.exceptions import ValidationError


class Discount(TimeStampedModel):
    DISCOUNT_TYPE_CHOICES = (
        ("percentage", "Percentage Off"),
        (
            "fixed",
            "Fixed Amount Off",
        ),
    )

    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="discounts",
        null=True,
        blank=True,
    )
    type = models.CharField(
        max_length=20,
        choices=DISCOUNT_TYPE_CHOICES,
    )
    code = models.CharField(max_length=50, unique=True)
    usage_limit = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    min_purchase_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    expire_at = models.DateTimeField()

    def clean(self):
        super().clean()
        if self.type == "percentage" and self.value > 100:
            raise ValidationError("Percentage discount cannot be greater than 100%.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class DiscountUsage(TimeStampedModel):
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="discount_usages",
    )
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="discount_usages"
    )
    discount = models.ForeignKey(
        Discount, on_delete=models.CASCADE, related_name="discount_usages"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    objects = DiscountUsageManager()
