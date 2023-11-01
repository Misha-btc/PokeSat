from django.contrib.auth.mixins import (
    UserPassesTestMixin,
    LoginRequiredMixin,
)
from django.shortcuts import redirect
from django.urls import reverse_lazy

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

    def handle_no_permission(self):
        return redirect(
            'blog:post_detail', post_id=self.kwargs[self.pk_url_kwarg]
        )

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile', kwargs={'username': self.request.user}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(
            self.request.POST or None,
            instance=self.object
        )
        return context


class CommentMixin(LoginRequiredMixin):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'post_id'

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs[self.pk_url_kwarg]}
        )
