from django.urls import path
from .views import create_task_view, update_task_status, get_tasks
from .views import dashboard_view

urlpatterns = [
    path('create/', create_task_view),
    path('<int:task_id>/update/', update_task_status),
    path('', get_tasks),
    path('dashboard/', dashboard_view),
]