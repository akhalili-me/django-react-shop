from modules.utility.models import TimeStampedModel
from django.db.models import Sum, F
from django.db import models
from uuid import uuid4
from django.urls import reverse


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

    def clear_session(self):
        self.total = 0
        self.cart_items.all().delete()
        self.save()


class CartItem(TimeStampedModel):
    session = models.ForeignKey(
        ShoppingSession, null=True, on_delete=models.CASCADE, related_name="cart_items"
    )
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    uuid = models.UUIDField(default=uuid4, editable=False, db_index=True)

    def get_absolute_url(self):
        return reverse("cart:cart-item-detail", kwargs={"uuid": self.uuid})
