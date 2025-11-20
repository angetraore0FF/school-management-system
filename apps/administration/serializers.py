from rest_framework import serializers
from .models import SystemConfiguration, AuditLog, AcademicSetting
from apps.users.serializers import UserSerializer
from apps.academic.serializers import SchoolYearSerializer

class SystemConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemConfiguration
        fields = '__all__'

class AuditLogSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = AuditLog
        fields = '__all__'

class AcademicSettingSerializer(serializers.ModelSerializer):
    school_year_name = serializers.CharField(source='school_year.name', read_only=True)
    
    class Meta:
        model = AcademicSetting
        fields = '__all__'