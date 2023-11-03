import factory
from django.contrib.auth import get_user_model

__all__ = [
    "UserFactory",
    "SuperUserFactory",
]


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.django.make_password("testpass")

    class Meta:
        model = get_user_model()


class SuperUserFactory(UserFactory):
    is_superuser = True
    is_staff = True
