from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from .models import Post, Category
from .forms import EmailPostForm, CommentForm
from taggit.models import Tag
from django.db.models import Count, Q


def post_list(request, tag_slug=None, category_slug=None):
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {'page': page,
               'posts': posts,
               'tag': tag}
    return render(request, 'blog/post/list.html', context)


def post_search(request):
    if request.method == "GET":
        query = request.GET.get('search')
        submit_button = request.GET.get('submit')

        if query is not None:
            lookups = Q(title__icontains=query) | Q(content__icontains=query)
            results = Post.objects.filter(lookups).distinct().order_by('-publish')
            context = {'posts': results,
                       'submit_button': submit_button}
            return render(request, 'blog/post/list.html', context)
        else:
            return render(request, 'blog/post/list.html')
    else:
        return render(request, 'blog/post/list.html')


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    context = {'post': post,
               'comments': comments,
               'new_comment': new_comment,
               'comment_form': comment_form,
               'similar_posts': similar_posts}
    return render(request, 'blog/post/detail.html', context)


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} советует вам прочитать {post.title}"
            message = f"Прочитай {post.title} тут - {post_url}\n\n Комментарий от {cd['name']}: {cd['comments']}"
            send_mail(subject, message, 'timur3214t@gmail.com', [cd['to']], fail_silently=False)
            sent = True
    else:
        form = EmailPostForm()
        context = {'post': post,
                   'form': form,
                   'sent': sent}
    return render(request, 'blog/post/share.html', context)


def post_by_category(request, category_slug):
    # Сортировать статьи по категориям
    objects_list = Post.objects.filter(category__category_slug=category_slug).order_by('publish')
    if not objects_list:
        raise Http404("Категория не найдена")
    category = Category.objects.get(category_slug=category_slug)
    paginator = Paginator(objects_list, 5)
    page = request.GET.get('page')
    try:
        objects_list = paginator.page(page)
    except PageNotAnInteger:
        objects_list = paginator.page(1)
    except EmptyPage:
        objects_list = paginator.page(paginator.num_pages)
    context = {
        'category': category,
        'posts': objects_list,
        'page': page,
    }
    return render(request, 'blog/post/category.html', context)
