from django.db import models


class ShoppingSession(models.Model):
    user = models.OneToOneField(
        "accounts.User", on_delete=models.CASCADE, related_name="shopping_session"
    )
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update_total(self):
        total = 0
        cart_items = CartItem.objects.filter(session=self)
        for item in cart_items:
            total += item.product.price * item.quantity
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
    status = models.CharField(
        max_length=20,
        default="pending",
        choices=(("created", "Created"), ("paid", "Paid"), ("failed", "Failed")),
        db_index=True,
    )
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


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(
        "products.Product", on_delete=models.CASCADE, related_name="order_items"
    )
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Payment(models.Model):
    amount = models.BigIntegerField()
    status = models.CharField(
        max_length=20,
        default="created",
        choices=(("created", "Created"), ("paid", "Paid"), ("failed", "Failed")),
        db_index=True,
    )
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

    def get_full_address(self):
        return f"{self.house_number}, {self.street_address}, {self.city}, {self.state}, {self.postal_code}"
