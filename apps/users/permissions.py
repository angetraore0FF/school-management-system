from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_role('ADMIN')

class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_role('TEACHER')

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_role('STUDENT')

class IsAdminOrTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_role('ADMIN') or request.user.has_role('TEACHER')

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.has_role('ADMIN'):
            return True
        
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        return obj == request.user