from django.contrib import admin
from django.urls import path, include
from accounts.views import login_page, signup_page
from .views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('projects/', include('projects.urls')), 
    path('tasks/', include('tasks.urls')),
    path('', signup_page),
    path('login/', login_page),
]
