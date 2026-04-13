from . import views
from django.urls import path

urlpatterns = [
    path('users/<int:user_id>/', views.user_profile, name='user_profile'),
    path('feed/', views.post_feed, name='post_feed'),
    path('profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('', views.post_list, name='post_list'), 
    path('share_task/<int:task_id>/', views.share_task, name='share_task'),
    path('<int:pk>/', views.post_detail, name='post_detail'), 
    path('<int:pk>/like/', views.like_post, name='like_post'),
    path('<int:pk>/comments/', views.post_comments, name='post_comments'),
    path('google_callback/', views.google_callback, name='google_callback'),
]