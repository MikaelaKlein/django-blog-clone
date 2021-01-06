from django.shortcuts import render
from django.urls import reverse_lazy
from blog.models import (
    Post,
    Comment,
)
from blog.forms import (
    PostForm,
    CommentForm,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

# Create your views here.
class AboutView(TemplateView):
    template_name = 'about.html'


class PostListView(ListView):
    model = Post

    # Basically doing a SQL query on your model
    # It's saying, grab the "Post" model, and filter on these conditions

    # __lte appended to a field name means "less than or equal to"
    # dash in front of the "published_date" field in the order by means descending order
    # Checkout more of the "Field lookups" documentation here: https://docs.djangoproject.com/en/3.1/ref/models/querysets/#field-lookups
    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


class PostDetailView(DetailView):
    model = Post

# LoginRequiredMixin is the class-based view equivalent of the `login_required` decorator
# which only works on functions.
class CreatePostView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post


class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    # Use `reverse_lazy()` instead of just `reverse()` because I think it waits for
    # the post to be deleted before it redirects to the page specified.
    success_url = reverse_lazy('post_list')


class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')
