from django.db import models
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.URLField(default='')
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    profile_image = models.ImageField(upload_to='profiles', default='default.jpg')

    def __str__(self):
        return self.user.username

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'posts')
    post_title = models.CharField(max_length=200)
    post_text = RichTextField(blank=True, null=True)
    draft_state = models.BooleanField(default=False)
    post_created = models.DateTimeField(auto_now_add=True, auto_now=False, blank=True)
    post_published = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)

    def __str__(self):
        return self.post_title

    def get_absolute_url(request):
        return reverse('blog:showposts')

class CommentsTable(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post_title = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    comment_text = models.CharField(max_length=240)
    comment_created = models.DateTimeField(auto_now_add=True, auto_now=False, blank=True)
    comment_state = models.BooleanField(default=False)
