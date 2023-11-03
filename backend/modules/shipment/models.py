from django.db import models
from modules.utility.models import TimeStampedModel
from uuid import uuid4
from .managers import BillingAddressManager
from django.urls import reverse


class Address(TimeStampedModel):
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    phone = models.CharField(unique=True)
    postal_code = models.CharField(max_length=10)
    street_address = models.TextField(max_length=250)
    house_number = models.CharField(max_length=15)
    uuid = models.UUIDField(default=uuid4, editable=False, db_index=True)

    def __str__(self):
        return f"{self.state}, {self.city}, {self.street_address}, Pelak: {self.house_number}, Postal Code: {self.postal_code}"

    class Meta:
        abstract = True


class UserAddress(Address):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("shipment:user-address-detail", kwargs={"uuid": self.uuid})


class BillingAddress(Address):
    objects = BillingAddressManager()


class State(TimeStampedModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class City(TimeStampedModel):
    name = models.CharField(max_length=50)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="cities")

    def __str__(self):
        return self.name
