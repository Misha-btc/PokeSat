from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.views.generic import (
    CreateView,
    DeleteView,
    UpdateView,
    ListView,
)

from .forms import CommentForm, PostForm, UserProfileForm
from .models import Category, Post, User
from .constants import POSTS_LIMIT, COMMENTS_LIMIT
from .mixin import (
    CommentMixin,
    PostMixin,
    CheckAuthorMixin,
    comment_count,
    filter_post,
)


class UserCreateView(CreateView):
    template_name = 'registration/registration_form.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('pages:rules')


class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class PostDetailView(ListView):
    model = Post
    template_name = 'blog/detail.html'
    paginate_by = COMMENTS_LIMIT

    def get_object(self):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        if post.author == self.request.user:
            return post
        else:
            return get_object_or_404(
                Post,
                pk=post_id,
                is_published=True,
                category__is_published=True,
                pub_date__lt=now()
            )

    def get_queryset(self):
        queryset = self.get_object().comments.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['post'] = self.get_object()
        return context


class PostUpdateView(PostMixin, UpdateView):

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.get_object().id}
        )


class PostDeleteView(PostMixin, DeleteView):
    pass


class CommentUpdateView(CheckAuthorMixin, CommentMixin, UpdateView):
    template_name = 'blog/comment.html'


class CommentDeleteView(CommentMixin, CheckAuthorMixin, DeleteView):
    template_name = 'blog/comment.html'


class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = POSTS_LIMIT

    def get_queryset(self):
        queryset = comment_count(filter_post(Post.objects.all()))
        return queryset


class ProfileDetailView(ListView):
    model = User
    template_name = 'blog/profile.html'
    paginate_by = POSTS_LIMIT

    def get_profile(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_queryset(self):
        queryset = comment_count(
            self.get_profile().posts.all().order_by('-pub_date')
        )
        if self.request.user != self.get_profile():
            queryset = filter_post(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_profile()
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserProfileForm
    model = User
    template_name = 'blog/user.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.kwargs[self.slug_url_kwarg]}
        )


class CategoryDetailView(ListView):
    model = Category
    template_name = 'blog/category.html'
    paginate_by = 10

    def get_category(self):
        return get_object_or_404(
            Category,
            slug=self.kwargs.get('category_slug'),
            is_published=True
        )

    def get_queryset(self):
        return comment_count(
            filter_post(
                self.get_category().posts.all().order_by('-pub_date')
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.get_category()
        return context


class AddComment(CommentMixin, CreateView):

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return super().form_valid(form)
