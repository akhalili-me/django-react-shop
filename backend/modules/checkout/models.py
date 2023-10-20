from django.db import models
from modules.utility.models import TimeStampedModel

class Payment(TimeStampedModel):
    STATUS_CHOICES = (("pending", "Pending"), ("paid", "Paid"), ("failed", "Failed"))

    amount = models.BigIntegerField()
    payment_method = models.CharField(max_length=200)
    status = models.CharField(
        max_length=20,
        default="pending",
        choices=STATUS_CHOICES,
        db_index=True,
    )
    paid_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)