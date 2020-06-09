from django.contrib import admin
from blog.models import Post, UserProfile, CommentsTable

# Register your models here.
admin.site.register(Post)
admin.site.register(UserProfile)
admin.site.register(CommentsTable)
