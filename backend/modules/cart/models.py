from modules.utility.models import TimeStampedModel
from django.db.models import Sum, F
from django.db import models
from .managers import (
    OrderItemManager,
    OrderManager,
)


class ShoppingSession(TimeStampedModel):
    user = models.OneToOneField(
        "accounts.User", on_delete=models.CASCADE, related_name="shopping_session"
    )
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def update_total(self):
        total = (
            self.cart_items.aggregate(
                total_price=Sum(F("product__price") * F("quantity"))
            )["total_price"]
            or 0
        )
        self.total = total
        self.save()


class CartItem(TimeStampedModel):
    session = models.ForeignKey(
        ShoppingSession, null=True, on_delete=models.CASCADE, related_name="cart_items"
    )
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    quantity = models.IntegerField()


class Order(TimeStampedModel):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    address = models.ForeignKey("Address", null=True, on_delete=models.CASCADE)
    shipping_price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    payment = models.OneToOneField(
        "Payment", on_delete=models.CASCADE, related_name="order"
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


class Address(TimeStampedModel):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    phone = models.CharField(max_length=11, unique=True)
    postal_code = models.CharField(max_length=10)
    street_address = models.TextField(max_length=250)
    house_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.state}, {self.city}, {self.street_address}, Pelak: {self.house_number}, Postal Code: {self.postal_code}"


class State(TimeStampedModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class City(TimeStampedModel):
    name = models.CharField(max_length=50)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="cities")

    def __str__(self):
        return self.name
