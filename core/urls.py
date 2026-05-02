from django.contrib import admin
from .views import home
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('projects/', include('projects.urls')), 
    path('tasks/', include('tasks.urls')),
    path('', home),
]
