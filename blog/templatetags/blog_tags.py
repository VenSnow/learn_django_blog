from django import template
from django.db.models import Count
from ..models import Post

register = template.Library()


@register.simple_tag(name='posts_count')
def total_posts():
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html', name='latest_posts')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.inclusion_tag('blog/post/commented_posts.html', name='commented_posts')
def get_most_commented_posts(count=3):
    commented_posts = Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]
    return {'commented_posts': commented_posts}
