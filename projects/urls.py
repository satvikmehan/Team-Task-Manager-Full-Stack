from django.urls import path
from .views import (
    add_members_view,
    create_project_page,
    create_project_view,
    edit_project_page,
    get_projects,
    project_manage_page,
    project_members_page,
)

urlpatterns = [
    path('', get_projects),
    path('create/', create_project_view),
    path('new/', create_project_page),
    path('manage/', project_manage_page),
    path('<int:project_id>/edit/', edit_project_page),
    path('<int:project_id>/members/', project_members_page),
    path('<int:project_id>/add-members/', add_members_view),
]
