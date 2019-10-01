from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    name = models.CharField(max_length=64)
    text = models.CharField(max_length=255)
    likes = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)

    def author_name(self):
        return self.author.username
