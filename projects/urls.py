from django.urls import path

from django.urls import path
from .views import project_list_page, create_project_page, add_members_page

urlpatterns = [
    path('', project_list_page),
    path('create/', create_project_page),
    path('<int:project_id>/add-members/', add_members_page),
]