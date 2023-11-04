# Generated by Django 4.2.5 on 2023-10-29 19:03

from django.db import migrations
import modules.utility.custom_fields


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0004_category_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="slug",
            field=modules.utility.custom_fields.AutoSlugField(
                blank=True,
                editable=False,
                max_length=128,
                populate_from="name",
                unique=True,
            ),
        ),
    ]