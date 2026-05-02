from django.urls import path
from .views import test_protected
from .views import create_project_view, get_projects
from .views import add_members_view

urlpatterns = [
    path('test/', test_protected),
    path('create/', create_project_view),
    path('', get_projects),
    path('<int:project_id>/add-members/', add_members_view),
]