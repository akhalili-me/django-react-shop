# Generated by Django 4.0.6 on 2023-03-04 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_comment_created_at_comment_updated_at_feature'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(default='exit', upload_to=None),
            preserve_default=False,
        ),
    ]
