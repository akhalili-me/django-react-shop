from modules.utility.models import TimeStampedModel
from django.core.validators import MaxValueValidator
from django.db import models
from .managers import ReportManager
from uuid import uuid4
from django.urls import reverse


class Comment(TimeStampedModel):
    product = models.ForeignKey(
        "products.Product", on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    rate = models.IntegerField(validators=[MaxValueValidator(5)])
    uuid = models.UUIDField(default=uuid4, editable=False, db_index=True)

    def __str__(self):
        return f"{self.text}"

    def get_absolute_url(self):
        return reverse("reviews:comment-detail", kwargs={"uuid": self.uuid})


class Like(TimeStampedModel):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid4, db_index=True, editable=False)

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
    uuid = models.UUIDField(default=uuid4, db_index=True, editable=False)

    objects = ReportManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "comment"], name="unique_report")
        ]

    def get_absolute_url(self):
        return reverse("reviews:report-detail", kwargs={"uuid": self.uuid})
