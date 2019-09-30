from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    name = models.CharField(max_length=64)
    text = models.CharField(max_length=255)
    likes = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)