from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import SystemConfiguration, AuditLog, AcademicSetting
from .serializers import SystemConfigurationSerializer, AuditLogSerializer, AcademicSettingSerializer
from apps.users.permissions import IsAdmin

class SystemConfigurationListCreateView(generics.ListCreateAPIView):
    queryset = SystemConfiguration.objects.all()
    serializer_class = SystemConfigurationSerializer
    permission_classes = [IsAdmin]

class SystemConfigurationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SystemConfiguration.objects.all()
    serializer_class = SystemConfigurationSerializer
    permission_classes = [IsAdmin]

class AuditLogListView(generics.ListAPIView):
    queryset = AuditLog.objects.all().order_by('-timestamp')
    serializer_class = AuditLogSerializer
    permission_classes = [IsAdmin]

class AcademicSettingListCreateView(generics.ListCreateAPIView):
    queryset = AcademicSetting.objects.all()
    serializer_class = AcademicSettingSerializer
    permission_classes = [IsAdmin]

@api_view(['GET'])
@permission_classes([IsAdmin])
def system_overview(request):
    from apps.users.models import User
    from apps.academic.models import SchoolYear, Class, Subject
    
    total_users = User.objects.count()
    total_teachers = User.objects.filter(roles__name='TEACHER').count()
    total_students = User.objects.filter(roles__name='STUDENT').count()
    total_classes = Class.objects.count()
    total_subjects = Subject.objects.count()
    active_school_year = SchoolYear.objects.filter(is_active=True).first()
    
    return Response({
        'total_users': total_users,
        'total_teachers': total_teachers,
        'total_students': total_students,
        'total_classes': total_classes,
        'total_subjects': total_subjects,
        'active_school_year': active_school_year.name if active_school_year else None,
    })