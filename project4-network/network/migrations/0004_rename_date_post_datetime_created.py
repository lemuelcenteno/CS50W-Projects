# Generated by Django 4.0.5 on 2022-06-23 03:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("network", "0003_post_date"),
    ]

    operations = [
        migrations.RenameField(
            model_name="post",
            old_name="date",
            new_name="datetime_created",
        ),
    ]
