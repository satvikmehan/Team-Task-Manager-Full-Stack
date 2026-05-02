from django.contrib import admin
from .views import home
from django.urls import path, include
from accounts.views import signup_page, login_page, dashboard_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('projects/', include('projects.urls')), 
    path('tasks/', include('tasks.urls')),
    path('', login_page),
    path('signup/', signup_page),
    path('dashboard/', dashboard_page),
]