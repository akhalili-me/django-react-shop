# Generated by Django 4.1.7 on 2023-04-03 14:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0009_commentlike_unique_comment_like"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="sold",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="product",
            name="views",
            field=models.IntegerField(default=0),
        ),
    ]