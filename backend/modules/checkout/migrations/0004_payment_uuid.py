# Generated by Django 4.2.5 on 2023-11-03 19:51

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("checkout", "0003_payment_description_payment_is_main_payment"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="uuid",
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False),
        ),
    ]
