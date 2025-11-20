from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Role

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    list_filter = ['name']

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'get_primary_role', 'is_active']
    list_filter = ['roles', 'is_active', 'is_staff']
    filter_horizontal = ['roles', 'groups', 'user_permissions']
    
    def get_primary_role(self, obj):
        return obj.get_primary_role()
    get_primary_role.short_description = 'Rôle Principal'