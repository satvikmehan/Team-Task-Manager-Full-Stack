from django.urls import path
from .views import add_members_view, create_project_page, create_project_view, get_projects

urlpatterns = [
    path('', get_projects),
    path('create/', create_project_view),
    path('new/', create_project_page),
    path('<int:project_id>/add-members/', add_members_view),
]
