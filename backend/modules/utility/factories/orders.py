import factory
from factory.django import DjangoModelFactory
from ..loading import get_model

__all__ = [
    "OrderFactory",
    "OrderItemFactory",
]


class OrderFactory(DjangoModelFactory):
    user = factory.SubFactory("modules.utility.factories.UserFactory")
    billing_address = factory.SubFactory(
        "modules.utility.factories.BillingAddressFactory"
    )
    shipping_price = factory.Faker(
        "pydecimal", left_digits=4, right_digits=2, positive=True
    )
    total = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
    status = "delivered"

    class Meta:
        model = get_model("orders", "Order")


class OrderItemFactory(DjangoModelFactory):
    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory("modules.utility.factories.ProductFactory")
    quantity = factory.Faker("random_int", min=1, max=10)

    class Meta:
        model = get_model("orders", "OrderItem")
