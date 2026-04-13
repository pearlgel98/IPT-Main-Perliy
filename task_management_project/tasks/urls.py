from django.urls import path
from djanago.http import JsonResponse
from .views import get_task

def test(request):
    return JsonResonpse({"message": "WORKING"})
urlpatterns = [
    path('test/', test),
    path('<int:task_id>/', get_task),
]