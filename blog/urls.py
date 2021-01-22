from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('posts/<slug:slug>', views.post_detail, name='post_detail'),
    path('posts/<int:post_id>/share/', views.post_share, name='post_share'),
    path('search/', views.post_search, name='post_search'),
    path('category/<slug:category_slug>/', views.post_by_category, name='post_by_category'),
    path('resume/', views.resume_page, name='resume_page'),
    path('contacts/', views.contacts_page, name='contacts_page'),
]
