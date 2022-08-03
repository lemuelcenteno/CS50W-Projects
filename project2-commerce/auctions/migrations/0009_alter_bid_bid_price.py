# Generated by Django 4.0.5 on 2022-06-16 04:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0008_alter_watchlist_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bid",
            name="bid_price",
            field=models.FloatField(
                validators=[django.core.validators.MinValueValidator(0)]
            ),
        ),
    ]