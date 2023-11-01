from django.db import models
from django.contrib.auth import get_user_model

from .constants import MAX_LENGTH, SLICE_TEXT

User = get_user_model()


class CreatedAtModel(models.Model):
    created_at = models.DateTimeField(
        'Добавлено',
        auto_now_add=True
    )

    class Meta:
        abstract = True
        ordering = ('created_at',)


class IsPublishedModel(CreatedAtModel):
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )

    class Meta(CreatedAtModel.Meta):
        abstract = True


class Location(IsPublishedModel):
    name = models.CharField('Название места', max_length=MAX_LENGTH)

    class Meta(IsPublishedModel.Meta):
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name[:SLICE_TEXT]


class Category(IsPublishedModel):
    title = models.CharField('Заголовок', max_length=MAX_LENGTH)
    description = models.TextField('Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text='Идентификатор страницы для URL; '
                  'разрешены символы латиницы, цифры, '
                  'дефис и подчёркивание.'
    )

    class Meta(IsPublishedModel.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title[:SLICE_TEXT]


class Post(IsPublishedModel):
    title = models.CharField('Заголовок', max_length=MAX_LENGTH)
    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text='Если установить дату и время в '
                  'будущем — можно делать отложенные публикации.'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение'
    )
    image = models.ImageField('Фото', upload_to='post_images', blank=True)

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        default_related_name = 'posts'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title[:SLICE_TEXT]


class Comment(CreatedAtModel):
    text = models.TextField('Оставьте ваш комментарий')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Публикация',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария',
    )

    class Meta(CreatedAtModel.Meta):
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'

    def __str__(self):
        return self.text[:SLICE_TEXT]
