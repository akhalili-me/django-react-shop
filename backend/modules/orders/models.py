from django.db import models
from modules.utility.models import TimeStampedModel
from .managers import (
    OrderItemManager,
)
from django.urls import reverse
from uuid import uuid4


class Order(TimeStampedModel):
    STATUS_CHOICES = (
        ("pending_payment", "Pending Payment"),
        ("delivered", "Delivered"),
        ("canceled", "Canceled"),
        ("completed", "Completed"),
    )

    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    billing_address = models.ForeignKey(
        "shipment.BillingAddress",
        null=True,
        on_delete=models.CASCADE,
        related_name="order",
    )
    shipping_price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=30, choices=STATUS_CHOICES, default="pending_payment"
    )
    uuid = models.UUIDField(default=uuid4, db_index=True, editable=False)

    def update_status(self, status):
        self.status = status
        self.save()

    def get_absolute_url(self):
        return reverse("orders:detail", kwargs={"uuid": self.uuid})


class OrderItem(TimeStampedModel):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
    )
    quantity = models.IntegerField(default=1)
    uuid = models.UUIDField(default=uuid4, db_index=True, editable=False)

    objects = OrderItemManager()

    def get_absolute_url(self):
        return reverse("orders:order-item-detail", kwargs={"uuid": self.uuid})
