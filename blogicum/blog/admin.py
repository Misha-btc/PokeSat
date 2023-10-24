from django.contrib import admin

from .models import Category, Post, Location

admin.site.empty_value_display = 'Не задано'


class PostInline(admin.TabularInline):
    model = Post
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'is_published',
        'created_at',
        'category',
        'location',
        'pub_date',
        'author'
    )
    list_editable = (
        'is_published',
        'category'
    )
    search_fields = ('title',)
    list_filter = ('category',)
    list_display_links = ('title',)
    raw_id_fields = ('author',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = (
        PostInline,
    )
    search_fields = ('title',)
    list_filter = ('created_at',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ('created_at',)
