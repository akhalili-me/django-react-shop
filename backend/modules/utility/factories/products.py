from modules.utility.loading import get_model
import factory

__all__ = [
    "ParentCategoryFactory",
    "ChildCategoryFactory",
    "ProductFactory",
    "ProductImageFactory",
    "FeatureFactory",
]


class ParentCategoryFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")
    image = factory.django.ImageField()
    parent = None

    class Meta:
        model = get_model("products", "Category")


class ChildCategoryFactory(ParentCategoryFactory):
    parent = factory.SubFactory(ParentCategoryFactory)


class ProductFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("sentence", nb_words=4)
    description = factory.Faker("text")
    price = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
    rate = factory.Faker(
        "pydecimal", left_digits=1, right_digits=1, positive=True, max_value=5
    )
    quantity = factory.Faker("random_int", min=50, max=100)
    sold = factory.Faker("random_int", min=0, max=100)
    views = factory.Faker("random_int", min=0, max=100)

    category = factory.SubFactory(ChildCategoryFactory)

    class Meta:
        model = get_model("products", "Product")


class ProductImageFactory(factory.django.DjangoModelFactory):
    product = factory.SubFactory(ProductFactory)
    name = factory.Faker("file_name")
    image = factory.django.ImageField(width=100, height=100)

    class Meta:
        model = get_model("products", "ProductImage")


class FeatureFactory(factory.django.DjangoModelFactory):
    product = factory.SubFactory(ProductFactory)
    name = factory.Faker("word")
    description = factory.Faker("text", max_nb_chars=500)

    class Meta:
        model = get_model("products", "Feature")
