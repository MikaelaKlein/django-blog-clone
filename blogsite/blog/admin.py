from django.contrib import admin
from blog.models import Post, Comment

# Register your models here.
# You must "register" your models here after making them so the Django knows they exist
admin.site.register(Post)
admin.site.register(Comment)
