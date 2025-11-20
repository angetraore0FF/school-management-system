from rest_framework import permissions

class HasRole(permissions.BasePermission):
    def __init__(self, role_name):
        self.role_name = role_name

    def has_permission(self, request, view):
        return request.user.has_role(self.role_name)

class IsAdminOrTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_role('ADMIN') or request.user.has_role('TEACHER')