from django.urls import path
from .views import google_callback, google_logout

urlpatterns = [
    path('callback/', google_callback, name='google_callback'),
    path('logout/', google_logout, name='google_logout'),
]