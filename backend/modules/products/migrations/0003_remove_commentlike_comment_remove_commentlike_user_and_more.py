# Generated by Django 4.2.5 on 2023-10-18 17:15

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0002_commentlike_updated_at"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="commentlike",
            name="comment",
        ),
        migrations.RemoveField(
            model_name="commentlike",
            name="user",
        ),
        migrations.DeleteModel(
            name="Comment",
        ),
        migrations.DeleteModel(
            name="CommentLike",
        ),
    ]
