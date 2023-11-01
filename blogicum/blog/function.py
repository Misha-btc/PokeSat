from django.utils.timezone import now
from django.db.models import Count


def comment_count(queryset):
    return queryset.select_related(
        'author', 'location', 'category'
    ).annotate(
        comments_count=Count('comments')
    ).order_by('-pub_date')


def filter_post(queryset):
    return queryset.filter(
        is_published=True,
        category__is_published=True,
        pub_date__lt=now()
    )
