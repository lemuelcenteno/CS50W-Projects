# Generated by Django 4.0.5 on 2022-06-23 07:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("network", "0005_user_followers"),
    ]

    operations = [
        migrations.RenameField(
            model_name="post",
            old_name="datetime_created",
            new_name="timestamp",
        ),
    ]