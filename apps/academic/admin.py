from django.contrib import admin
from .models import SchoolYear, Subject, Class, ClassAssignment, StudentEnrollment, Grade, Attendance

@admin.register(SchoolYear)
class SchoolYearAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date', 'is_active']
    list_filter = ['is_active']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['name', 'code']

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'capacity', 'school_year']
    list_filter = ['school_year']

@admin.register(ClassAssignment)
class ClassAssignmentAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'subject', 'class_obj', 'school_year']
    list_filter = ['school_year', 'subject']

@admin.register(StudentEnrollment)
class StudentEnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'class_obj', 'school_year', 'enrollment_date']
    list_filter = ['school_year', 'class_obj']

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'class_obj', 'grade_type', 'value', 'date_given']
    list_filter = ['grade_type', 'subject', 'class_obj']

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'class_obj', 'date', 'period', 'is_present']
    list_filter = ['date', 'is_present', 'class_obj']