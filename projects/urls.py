from django.urls import path
from .views import add_members_view, create_project_view, get_projects

urlpatterns = [
    path('', get_projects),
    path('create/', create_project_view),
    path('<int:project_id>/add-members/', add_members_view),
]
