from rest_framework import serializers
from apps.users.models import User
from apps.academic.models import ClassAssignment, Grade, Attendance
from apps.users.serializers import UserSerializer

class DashboardStatsSerializer(serializers.Serializer):
    total_users = serializers.IntegerField()
    total_teachers = serializers.IntegerField()
    total_students = serializers.IntegerField()
    total_classes = serializers.IntegerField()
    total_subjects = serializers.IntegerField()
    active_school_year = serializers.CharField(allow_null=True)

class TeacherDashboardSerializer(serializers.Serializer):
    classes_count = serializers.IntegerField()
    subjects_count = serializers.IntegerField()
    students_count = serializers.IntegerField()
    recent_grades = serializers.IntegerField(default=0)
    recent_attendances = serializers.IntegerField(default=0)

class LoginResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserSerializer()
    dashboard_url = serializers.CharField()