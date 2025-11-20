from django.contrib import admin
from .models import SystemConfiguration, AuditLog, AcademicSetting

@admin.register(SystemConfiguration)
class SystemConfigurationAdmin(admin.ModelAdmin):
    list_display = ['key', 'value', 'description']
    search_fields = ['key']

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'model_name', 'timestamp']
    list_filter = ['action', 'timestamp']
    readonly_fields = ['user', 'action', 'model_name', 'object_id', 'details', 'ip_address', 'timestamp']

@admin.register(AcademicSetting)
class AcademicSettingAdmin(admin.ModelAdmin):
    list_display = ['school_year', 'setting_key', 'setting_value']
    list_filter = ['school_year']