from django.urls import path
from .views import *

urlpatterns = [
    # Routes administration
    path('school-years/', SchoolYearListCreateView.as_view(), name='schoolyear-list-create'),
    path('subjects/', SubjectListCreateView.as_view(), name='subject-list-create'),
    path('classes/', ClassListCreateView.as_view(), name='class-list-create'),
    path('assignments/', ClassAssignmentListCreateView.as_view(), name='assignment-list-create'),
    path('enrollments/', StudentEnrollmentListCreateView.as_view(), name='enrollment-list-create'),
    
    # Routes enseignants
    path('teacher/assignments/', TeacherClassAssignmentListView.as_view(), name='teacher-assignments'),
    path('teacher/grades/', TeacherGradeListCreateView.as_view(), name='teacher-grades'),
    path('teacher/attendances/', TeacherAttendanceListCreateView.as_view(), name='teacher-attendances'),
]