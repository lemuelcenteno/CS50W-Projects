# Generated by Django 4.0.5 on 2022-06-16 14:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_rename_comment_comment_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='date_created',
        ),
        migrations.AddField(
            model_name='bid',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='listing',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
