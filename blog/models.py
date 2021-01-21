from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Черновик'),
        ('published', 'Опубликован')
    )
    title = models.CharField(max_length=150, verbose_name='Название')
    slug = models.SlugField(max_length=160, unique=True, verbose_name='Слаг')
    category = models.ForeignKey('Category',
                                 on_delete=models.SET_NULL,
                                 related_name='category',
                                 null=True,
                                 verbose_name='Категория')
    author = models.ForeignKey(User,
                               related_name='blog_posts',
                               on_delete=models.CASCADE,
                               verbose_name='Автор')
    image = models.ImageField(upload_to='images/posts/',
                              default='images/default.jpg',
                              verbose_name='Постер')
    content = models.TextField(verbose_name='Контент')
    publish = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft',
                              verbose_name='Статус')
    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    category_slug = models.SlugField(unique=True, verbose_name='Слаг')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:post_by_category', kwargs={'category_slug': self.category_slug})


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments',
                             verbose_name='Пост')
    name = models.CharField(max_length=80, verbose_name='Имя')
    email = models.EmailField(verbose_name='E-mail')
    content = models.TextField(verbose_name='Текст')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлён')
    active = models.BooleanField(default=False, verbose_name='Активный')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-created',)

    def __str__(self):
        return f'Комментарий от {self.name} - {self.post}'


class PostPics(models.Model):
    alt = models.CharField(max_length=255, verbose_name='Название')
    image = models.ImageField(upload_to='images/posts/pics', verbose_name='Изображение')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост')

    def __str__(self):
        return f"{self.alt} - {self.post.title}"

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
