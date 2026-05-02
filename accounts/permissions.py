from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'ADMIN'


class IsMember(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'MEMBER'


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET']:
            return True
        return request.user.role == 'ADMIN'