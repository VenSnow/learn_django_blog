from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget
from django.utils.safestring import mark_safe

from .models import Post, Comment, Category, PostPics


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Post
        fields = '__all__'


class ImagesInline(admin.StackedInline):
    """Кадры из фильма"""
    model = PostPics
    extra = 1
    fields = ('image', 'get_image')
    readonly_fields = ('get_image',)
    classes = ['collapse']

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="350" height="260"')

    get_image.short_description = "Изображение"


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'publish', 'status',)
    list_filter = ('category', 'status', 'created', 'publish', 'author',)
    search_fields = ('title', 'body',)
    inlines = [ImagesInline, ]
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ['status', '-publish']
    form = PostAdminForm
    readonly_fields = ('get_image',)

    fieldsets = (
        (None, {
            'fields': (('title', 'author', ),)
        }),
        (None, {
            'fields': (('category', 'tags', ),)
        }),
        (None, {
            'fields': ('content', 'get_image', 'image')
        }),
        ('Options', {
            'fields': (('slug', 'publish', 'status'),)
        }),
    )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="260" height="350"')

    get_image.short_description = "Изображение"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active',)
    list_editable = ('active',)
    list_filter = ('active', 'created', 'updated',)
    search_fields = ('name', 'email', 'body',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_slug',)
    prepopulated_fields = {'category_slug': ('name',)}
    search_fields = ('name',)
