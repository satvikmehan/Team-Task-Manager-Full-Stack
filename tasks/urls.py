from django.urls import path
from .views import (
    create_task_page,
    create_task_view,
    dashboard_view,
    delete_task_page,
    edit_task_page,
    get_tasks,
    manage_tasks_page,
    update_task_status,
    update_task_status_page,
)

urlpatterns = [
    path('new/', create_task_page),
    path('manage/', manage_tasks_page),
    path('create/', create_task_view),
    path('<int:task_id>/edit/', edit_task_page),
    path('<int:task_id>/delete/', delete_task_page),
    path('<int:task_id>/status/', update_task_status_page),
    path('<int:task_id>/update/', update_task_status),
    path('', get_tasks),
    path('dashboard/', dashboard_view),
]
