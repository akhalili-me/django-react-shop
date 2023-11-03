import factory
from factory.django import DjangoModelFactory
from ..loading import get_model

__all__ = [
    "DiscountFactory",
    "DiscountUsageFactory",
]


class DiscountFactory(DjangoModelFactory):
    name = factory.Faker("word")
    user = factory.SubFactory("modules.utility.factories.UserFactory")
    type = "percentage"
    code = factory.Faker("uuid4")
    usage_limit = 1
    is_active = True
    value = factory.Faker(
        "pydecimal", left_digits=4, right_digits=2, positive=True, max_value=100
    )
    min_purchase_amount = None
    expire_at = factory.Faker("future_datetime")

    class Meta:
        model = get_model("discounts", "Discount")


class DiscountUsageFactory(DjangoModelFactory):
    user = factory.SubFactory("modules.utility.factories.UserFactory")
    order = factory.SubFactory("modules.utility.factories.OrderFactory")
    discount = factory.SubFactory(DiscountFactory, user=None)
    amount = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)

    class Meta:
        model = get_model("discounts", "DiscountUsage")
