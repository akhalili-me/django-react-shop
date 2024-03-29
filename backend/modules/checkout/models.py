from django.db import models
from modules.utility.models import TimeStampedModel
from uuid import uuid4
from django.urls import reverse


class Payment(TimeStampedModel):
    STATUS_CHOICES = (("pending", "Pending"), ("paid", "Paid"), ("failed", "Failed"))

    amount = models.BigIntegerField()
    method = models.CharField(max_length=200)
    status = models.CharField(
        max_length=20,
        default="pending",
        choices=STATUS_CHOICES,
        db_index=True,
    )
    order = models.ForeignKey(
        "orders.Order", on_delete=models.CASCADE, related_name="payments"
    )
    paid_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    is_main_payment = models.BooleanField(default=False)
    description = models.TextField(max_length=300, null=True, blank=True)
    uuid = models.UUIDField(default=uuid4, editable=False, db_index=True)

    def get_absolute_url(self):
        return reverse("checkout:payment-detail", kwargs={"uuid": self.uuid})
