from collections.abc import Iterable
from modules.utility.models import TimeStampedModel
from django.core.validators import MaxValueValidator
import os
from uuid import uuid4
from django.utils.deconstruct import deconstructible
from django.db.models import Avg
from django.db import models
from modules.utility.custom_fields import AutoSlugField
from django.urls import reverse


@deconstructible
class PathAndRename(object):
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split(".")[-1]
        # set filename as random string
        filename = "{}.{}".format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)


product_image = PathAndRename("images/products")
category_image = PathAndRename("images/categories")

#########################
#########################


class Product(TimeStampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rate = models.DecimalField(
        validators=[MaxValueValidator(5)], max_digits=2, decimal_places=1, default=0
    )
    quantity = models.IntegerField(default=0)
    sold = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, related_name="products", db_index=True
    )
    slug = AutoSlugField(
        populate_from="name", max_length=128, unique=True, db_index=True
    )

    def __str__(self):
        return self.name

    def update_rate(self):
        comment_rates = self.comments.filter(rate__gt=0).aggregate(Avg("rate"))
        self.rate = comment_rates["rate__avg"] or 0
        self.save()

    def get_absolute_url(self):
        return reverse("products:detail", kwargs={"slug": self.slug})


class ProductImage(TimeStampedModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to=product_image)

    def __str__(self):
        return f"{self.image.url}"


class Category(TimeStampedModel):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="children"
    )
    image = models.ImageField(upload_to=category_image)
    slug = AutoSlugField(
        populate_from="name", max_length=128, unique=True, db_index=True
    )

    def __str__(self):
        return f"{self.name}"


class Feature(TimeStampedModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="features"
    )
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=500)

    def __str__(self):
        return f"{self.name}"
