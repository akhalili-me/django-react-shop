from modules.utility.models import TimeStampedModel
from django.core.validators import MaxValueValidator
from django.db import models
from modules.products.models import Product
from .managers import ReportManager


class Comment(TimeStampedModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    rate = models.IntegerField(validators=[MaxValueValidator(5)])

    def __str__(self):
        return f"{self.text}"


class Like(TimeStampedModel):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "comment"], name="unique_like")
        ]


class Report(TimeStampedModel):
    REASON_CHOICES = (
        ("spam", "Spam"),
        ("harassment", "Harassment"),
        ("inappropriate content", "Inappropriate Content"),
        ("other", "Other"),
    )

    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="reports"
    )
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    reason = models.CharField(max_length=50, choices=REASON_CHOICES)

    objects = ReportManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "comment"], name="unique_report")
        ]
