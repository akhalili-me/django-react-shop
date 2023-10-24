from django.db import models
from modules.utility.models import TimeStampedModel
from .managers import (
    OrderItemManager,
    OrderManager,
)
from modules.shipment.models import Address


class Order(TimeStampedModel):
    STATUS_CHOICES = (
        ("pending_payment", "Pending Payment"),
        ("delivered", "Delivered"),
        ("canceled", "Canceled"),
        ("completed", "Completed"),
    )

    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    address = models.ForeignKey(Address, null=True, on_delete=models.CASCADE)
    shipping_price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=30, choices=STATUS_CHOICES, default="pending_payment"
    )
    objects = OrderManager()

    def __str__(self):
        return (
            self.user.username
            + " | "
            + self.payment.status
            + " | "
            + str(self.created_at)
        )


class OrderItem(TimeStampedModel):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
    )
    quantity = models.IntegerField(default=1)

    objects = OrderItemManager()
