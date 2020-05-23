from django.db import models
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=200)
    post_text = models.TextField()
    post_created = models.DateTimeField(auto_now_add=True, auto_now=False, blank=True)
    post_published = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)
