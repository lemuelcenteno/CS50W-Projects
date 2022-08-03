from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField(
        "self", symmetrical=False, related_name="following"
    )


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=140)
    likes = models.ManyToManyField(User, related_name="likes")

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "timestamp": self.timestamp,
            "text": self.text,
            "likes": len(self.likes.all()),
        }
