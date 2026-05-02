from django.urls import path
from .views import change_role, signup_view, login_view
from rest_framework_simplejwt.views import TokenRefreshView
from .views import create_admin

urlpatterns = [
    path('signup/', signup_view),
    path('login/', login_view),
    path('change-role/<int:user_id>/', change_role),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('create-admin/', create_admin)
]