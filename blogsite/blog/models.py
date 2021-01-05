from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.

class Post(models.Model):
    # These are the columns of the database table
    author = models.ForeignKey('auth.User')  # author is connected to an actual superuser
    title = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now())
    published_date = models.DateTimeField(blank=True, null=True)

    # I'm not yet sure how this is used
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    # this either
    def approve_comments(self):
        # "comments" attribute can be accessed here by the `related_name` in the
        # Comments class for the post.
        # approved_comment is a field in the Comment class (below)
        return self.comments.filter(approved_comment=True)

    # Need a `get_absolute_url` method, by taking advantage of the reverse() function.
    # NOTE: it needs to be called `get_absolute_url` because it's what django looks for.
    # The idea behind this is that after the user creates a post or a comment,
    # where should the website take them?

    # We'll use detail views for the Post, and function views for the comments
    def get_absolute_url(self):
        # pk stands for primary key, which is created automatically for every
        # new post.
        return reverse("post_detail", kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('blog.post', related_name = 'comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now())
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        # Go back to the home page containing all the posts.
        return reverse('post_list')

    def __str__(self):
        return self.text
