from rest_framework import serializers
from .models import (
    SchoolYear, Subject, Class, ClassAssignment, 
    StudentEnrollment, Grade, Attendance
)
from apps.users.serializers import UserSerializer

class SchoolYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolYear
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class ClassSerializer(serializers.ModelSerializer):
    school_year_name = serializers.CharField(source='school_year.name', read_only=True)
    
    class Meta:
        model = Class
        fields = '__all__'

class ClassAssignmentSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.get_full_name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    class_name = serializers.CharField(source='class_obj.name', read_only=True)
    school_year_name = serializers.CharField(source='school_year.name', read_only=True)
    
    class Meta:
        model = ClassAssignment
        fields = '__all__'

class StudentEnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    class_name = serializers.CharField(source='class_obj.name', read_only=True)
    school_year_name = serializers.CharField(source='school_year.name', read_only=True)
    
    class Meta:
        model = StudentEnrollment
        fields = '__all__'

class GradeSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    class_name = serializers.CharField(source='class_obj.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = Grade
        fields = '__all__'
        read_only_fields = ['created_by']

class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    class_name = serializers.CharField(source='class_obj.name', read_only=True)
    recorded_by_name = serializers.CharField(source='recorded_by.get_full_name', read_only=True)
    
    class Meta:
        model = Attendance
        fields = '__all__'
        read_only_fields = ['recorded_by']