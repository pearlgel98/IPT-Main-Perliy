from django.urls import path
from . import views

urlpatterns = [
    path('feed/', views.post_feed, name='post_feed'),
    path('', views.post_list, name='post_list'), 
    path('<int:pk>/', views.post_detail, name='post_detail'), 
    path('<int:pk>/like/', views.like_post, name='like_post'),
    path('<int:pk>/comments/', views.post_comments, name='post_comments'),
]