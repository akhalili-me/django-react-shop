import factory
from factory.django import DjangoModelFactory
from ..loading import get_model

__all__ = [
    "CommentFactory",
    "LikeFactory",
    "ReportFactory",
]


class CommentFactory(DjangoModelFactory):
    product = factory.SubFactory("modules.utility.factories.ProductFactory")
    author = factory.SubFactory("modules.utility.factories.UserFactory")
    text = factory.Faker("text", max_nb_chars=500)
    rate = factory.Faker("random_int", min=1, max=5)

    class Meta:
        model = get_model("reviews", "Comment")


class LikeFactory(DjangoModelFactory):
    comment = factory.SubFactory(CommentFactory)
    user = factory.SubFactory("modules.utility.factories.UserFactory")

    class Meta:
        model = get_model("reviews", "Like")


class ReportFactory(DjangoModelFactory):
    comment = factory.SubFactory(CommentFactory)
    user = factory.SubFactory("modules.utility.factories.UserFactory")
    reason = factory.Faker(
        "random_element",
        elements=["spam", "harassment", "inappropriate content", "other"],
    )

    class Meta:
        model = get_model("reviews", "Report")
