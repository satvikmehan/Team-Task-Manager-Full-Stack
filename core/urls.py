from django.contrib import admin
from django.urls import path, include
from accounts.views import dashboard_page, login_page, signup_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('projects/', include('projects.urls')), 
    path('tasks/', include('tasks.urls')),
    path('', login_page),
    path('login/', login_page),
    path('signup/', signup_page),
    path('dashboard/', dashboard_page),
]
