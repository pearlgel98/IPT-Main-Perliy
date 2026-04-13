from .views import user_profile
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/posts/', include('posts.urls')), 
    path('api/auth/', include('authentication.urls')), 
    path('api/users/<int:user_id>/', user_profile, name='user-profile'),
    path('profile/<int:user_id>/', user_profile, name='user-profile'),
]