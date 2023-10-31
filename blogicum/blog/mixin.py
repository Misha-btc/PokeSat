from django.contrib.auth.mixins import (
    UserPassesTestMixin,
    LoginRequiredMixin,
)
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.db.models import Count

from .models import Comment, Post
from .forms import CommentForm, PostForm


class CheckAuthorMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user == self.get_object().author


class PostMixin(LoginRequiredMixin, CheckAuthorMixin):
    form_class = PostForm
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'blog/create.html'

    def get_object(self):
        return get_object_or_404(Post, pk=self.kwargs['post_id'])

    def handle_no_permission(self):
        return redirect('blog:post_detail', post_id=self.get_object().id)

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile', kwargs={'username': self.request.user}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = get_object_or_404(Post, pk=self.kwargs[self.pk_url_kwarg])
        form = PostForm(self.request.POST or None, instance=instance)
        context['form'] = form
        context['instance'] = instance
        context['post'] = self.get_object()
        return context


class CommentMixin(LoginRequiredMixin):
    model = Comment
    form_class = CommentForm
    template_name = 'includes/comments.html'

    def get_object(self):
        return get_object_or_404(
            Comment,
            post__id=self.kwargs['post_id'],
            id=self.kwargs['comment_id']
        )

    def get_success_url(self):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'post_id': post.id}
        )


def comment_count(queryset):
    return queryset.annotate(comments_count=Count('comments'))


def filter_post(queryset):
    return queryset.filter(
        is_published=True,
        category__is_published=True,
        pub_date__lt=now()
    ).order_by('-pub_date')
