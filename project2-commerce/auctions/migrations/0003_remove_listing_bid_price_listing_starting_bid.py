# Generated by Django 4.0.5 on 2022-06-15 04:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0002_alter_listing_bid_price"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="listing",
            name="bid_price",
        ),
        migrations.AddField(
            model_name="listing",
            name="starting_bid",
            field=models.FloatField(
                default=0,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name="Starting Bid",
            ),
        ),
    ]
