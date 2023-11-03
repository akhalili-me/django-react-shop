import factory
from factory.django import DjangoModelFactory
from ..loading import get_model

__all__ = [
    "ShoppingSessionFactory",
    "CartItemFactory",
]


class ShoppingSessionFactory(DjangoModelFactory):
    user = factory.SubFactory("modules.utility.factories.UserFactory")
    total = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)

    class Meta:
        model = get_model("cart", "ShoppingSession")


class CartItemFactory(DjangoModelFactory):
    session = factory.SubFactory(ShoppingSessionFactory)
    product = factory.SubFactory("modules.utility.factories.ProductFactory")
    quantity = factory.Faker("random_int", min=1, max=10)

    class Meta:
        model = get_model("cart", "CartItem")
