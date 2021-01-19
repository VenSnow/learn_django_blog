from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget

from .models import Post, Comment, Category


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Post
        fields = '__all__'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'publish', 'status',)
    list_filter = ('category', 'status', 'created', 'publish', 'author',)
    search_fields = ('title', 'body',)
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ['status', '-publish']
    form = PostAdminForm


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
