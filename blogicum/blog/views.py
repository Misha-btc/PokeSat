from typing import Any
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DetailView,
    DeleteView,
    UpdateView,
    ListView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.db.models import Q

from .forms import CommentForm, PostForm, UserProfileForm
from .models import Category, Comment, Post, User
from .constants import POSTS_LIMIT

now = timezone.now()


class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'blog/create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if post.pub_date > now:
            post.is_published = False
        else:
            post.is_published = True
        form.instance.author = self.request.user
        post.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get_object(self):
        post_id = self.kwargs.get('post_id')
        user = self.request.user
        try:
            post = Post.objects.get(pk=post_id)
            if self.can_view_post(user, post):
                return post
            else:
                raise Http404
        except Post.DoesNotExist:
            raise Http404

    def can_view_post(self, user, post):
        if user == post.author:
            return True
        else:
            return (post.is_published
                    and post.category.is_published
                    and post.pub_date < now
                    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments.select_related('author')
        )
        return context


class PostUpdateView(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'blog/create.html'

    def get_success_url(self):
        post = self.get_object()
        return reverse('blog:post_detail', kwargs={'post_id': post.id})

    def dispatch(self, request, *args, **kwargs: Any):
        post = get_object_or_404(Post, pk=kwargs['post_id'])
        if not request.user.is_authenticated:
            return HttpResponseRedirect(
                reverse(
                    'blog:post_detail',
                    kwargs={
                        'post_id': kwargs['post_id']
                    }
                )
            )
        if post.author != request.user:
            return HttpResponseRedirect(
                reverse(
                    'blog:post_detail',
                    kwargs={
                        'post_id': post.id
                    }
                )
            )
        return super().dispatch(request, *args, **kwargs)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'blog/create.html'

    def get_success_url(self):
        post = self.get_object()
        return reverse(
            'blog:profile',
            kwargs={
                'username': post.author.username
            }
        )

    def dispatch(self, request, *args, **kwargs: Any):
        if not request.user.is_authenticated:
            return redirect(reverse_lazy('login'))
        get_object_or_404(Post, pk=kwargs['post_id'], author=request.user)
        return super().dispatch(request, *args, **kwargs)


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    form_class = CommentForm
    model = Comment
    pk_url_kwarg = 'comment_id'
    template_name = 'blog/comment.html'

    def get_success_url(self):
        comment = self.get_object()
        return reverse('blog:post_detail', kwargs={'post_id': comment.post.id})

    def dispatch(self, request, *args, **kwargs: Any):
        comment = self.get_object()
        if comment.author != request.user:
            raise Http404("Вы не можете редактировать этот комментарий.")
        return super().dispatch(request, *args, **kwargs)


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    pk_url_kwarg = 'comment_id'
    template_name = 'blog/comment.html'

    def get_success_url(self):
        comment = self.get_object()
        return reverse('blog:post_detail', kwargs={'post_id': comment.post.id})

    def dispatch(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != request.user:
            raise Http404("Вы не можете удалить этот комментарий.")
        return super().dispatch(request, *args, **kwargs)


class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    ordering = '-pub_date'
    paginate_by = POSTS_LIMIT

    def get_queryset(self):
        queryset = Post.objects.filter(
            Q(is_published=True, category__is_published=True, pub_date__lt=now)
        )
        return queryset


class ProfileDetailView(DetailView):
    model = User
    template_name = 'blog/profile.html'

    def get_object(self):
        username = self.kwargs.get('username')
        profile = get_object_or_404(User, username=username)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['profile'] = profile
        user = self.request.user
        post_list = None
        if user.is_authenticated:
            if profile == user:
                post_list = Post.objects.filter(
                    author=profile).order_by('-pub_date')
            else:
                post_list = Post.objects.filter(Q(
                    author=profile,
                    is_published=True,
                    category__is_published=True,
                    pub_date__lt=now)).order_by('-pub_date')
        else:
            post_list = Post.objects.filter(Q(
                author=profile,
                is_published=True,
                category__is_published=True,
                pub_date__lt=now)).order_by('-pub_date')
        paginator = Paginator(post_list, POSTS_LIMIT)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context


class ProfileUpdateView(UpdateView):
    form_class = UserProfileForm
    model = User
    template_name = 'blog/user.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_success_url(self):
        user = self.get_object()
        return reverse('blog:profile', kwargs={'username': user.username})

    def dispatch(self, request, *args, **kwargs):
        user = self.get_object()
        profile = get_object_or_404(User, username=kwargs['username'])
        if user != request.user:
            return redirect('blog:profile', username=profile.username)
        return super().dispatch(request, *args, **kwargs)


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'blog/category.html'

    def get_object(self):
        slug = self.kwargs.get('category_slug')
        return Category.objects.get(slug=slug)

    def get_queryset(self):
        category = self.get_object()
        if not category.is_published:
            raise Http404("Категория не существует или снята с публикации.")
        queryset = Post.objects.filter(Q(
            is_published=True,
            category__is_published=True,
            pub_date__lt=now,
            category=category
        ))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_list = self.get_queryset().order_by('-pub_date')
        paginator = Paginator(post_list, POSTS_LIMIT)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', post_id=post_id)
