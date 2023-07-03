from django.db import models
from django.db.models import Sum, F
from django.db.models.signals import pre_save
from django.dispatch import receiver


class ShoppingSession(models.Model):
    user = models.OneToOneField(
        "accounts.User", on_delete=models.CASCADE, related_name="shopping_session"
    )
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update_total(self):
        total = (
            self.cart_items.aggregate(
                total_price=Sum(F("product__price") * F("quantity"))
            )["total_price"]
            or 0
        )
        self.total = total
        self.save()


class CartItem(models.Model):
    session = models.ForeignKey(
        ShoppingSession, null=True, on_delete=models.CASCADE, related_name="cart_items"
    )
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Order(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    address = models.ForeignKey("Address", null=True, on_delete=models.CASCADE)
    shipping_price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    payment = models.OneToOneField(
        "Payment", on_delete=models.CASCADE, related_name="order"
    )
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_total(self):
        # calculate the total amount of the order
        total = 0
        order_items = OrderItem.objects.filter(order=self)
        for item in order_items:
            total += item.product.price * item.quantity
        return total

    def __str__(self):
        return self.user.username + " | " + self.status + " | " + str(self.created_at)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(
        "products.Product", on_delete=models.CASCADE,
    )
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Payment(models.Model):
    amount = models.BigIntegerField()
    payment_method = models.CharField(max_length=200)
    status = models.CharField(
        max_length=20,
        default="pending",
        choices=(("pending", "Pending"), ("paid", "Paid"), ("failed", "Failed")),
        db_index=True,
    )
    paid_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Address(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    phone = models.CharField(max_length=11, unique=True)
    postal_code = models.CharField(max_length=10)
    street_address = models.TextField(max_length=250)
    house_number = models.CharField(max_length=15)

        
    def __str__(self):
        return f"{self.state}, {self.city}, {self.street_address}, Pelak: {self.house_number}, Postal Code: {self.postal_code}"

class State(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=50)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="cities")

    def __str__(self):
        return self.name
