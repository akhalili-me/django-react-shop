import factory
from factory import Faker
from ..loading import get_model

__all__ = [
    "StateFactory",
    "CityFactory",
    "BillingAddressFactory",
    "UserAddressFactory",
]


class StateFactory(factory.django.DjangoModelFactory):
    name = Faker("state")

    class Meta:
        model = get_model("shipment", "State")


class CityFactory(factory.django.DjangoModelFactory):
    name = Faker("city")
    state = factory.SubFactory(StateFactory)

    class Meta:
        model = get_model("shipment", "City")


class BillingAddressFactory(factory.django.DjangoModelFactory):
    state = Faker("state")
    city = factory.SubFactory(CityFactory)
    phone = Faker("phone_number")
    postal_code = Faker("postcode")
    street_address = Faker("street_address")
    house_number = Faker("building_number")

    class Meta:
        model = get_model("shipment", "BillingAddress")


class UserAddressFactory(BillingAddressFactory):
    user = factory.SubFactory("modules.utility.factories.UserFactory")

    class Meta:
        model = get_model("shipment", "UserAddress")
