from django.urls import path
from .views import *

urlpatterns = [
    path('system-config/', SystemConfigurationListCreateView.as_view(), name='system-config-list'),
    path('system-config/<int:pk>/', SystemConfigurationDetailView.as_view(), name='system-config-detail'),
    path('audit-logs/', AuditLogListView.as_view(), name='audit-logs'),
    path('academic-settings/', AcademicSettingListCreateView.as_view(), name='academic-settings'),
]