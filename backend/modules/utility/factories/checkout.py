import factory
from factory.django import DjangoModelFactory
from ..loading import get_model

__all__ = [
    "PaymentFactory",
]


class PaymentFactory(DjangoModelFactory):
    amount = factory.Faker("random_int", min=10, max=500)
    method = factory.Faker("word")
    status = "paid"
    order = factory.SubFactory("modules.utility.factories.OrderFactory")
    paid_at = factory.Faker("past_datetime")
    is_main_payment = True
    description = factory.Faker("text", max_nb_chars=300)

    class Meta:
        model = get_model("checkout", "Payment")
