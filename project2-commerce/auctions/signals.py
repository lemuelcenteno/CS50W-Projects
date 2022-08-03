from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model

from .models import Watchlist


@receiver(post_save, sender=get_user_model())
def create_user_watchlist(sender, instance, created, **kwargs):
    if created:
        Watchlist.objects.create(user=instance)
