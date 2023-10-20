from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from modules.accounts.managers import UserManager
from modules.utility.models import TimeStampedModel


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, db_index=True)
    username = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email


class Ban(TimeStampedModel):
    BAN_TYPE_CHOICES = (("comment", "Comment"), ("report", "Report"))

    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    ban_type = models.CharField(max_length=20, choices=BAN_TYPE_CHOICES)
    reason = models.TextField(null=True, blank=True)
    banned_until = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "ban_type"], name="unique_ban")
        ]
