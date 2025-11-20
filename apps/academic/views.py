from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q
from .models import *
from .serializers import *
from apps.users.permissions import IsAdmin, IsTeacher, IsAdminOrTeacher

# Vues pour l'administration (Admin seulement)
class SchoolYearListCreateView(generics.ListCreateAPIView):
    queryset = SchoolYear.objects.all()
    serializer_class = SchoolYearSerializer
    permission_classes = [IsAdmin]

class SubjectListCreateView(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAdmin]

class ClassListCreateView(generics.ListCreateAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [IsAdmin]

class ClassAssignmentListCreateView(generics.ListCreateAPIView):
    queryset = ClassAssignment.objects.all()
    serializer_class = ClassAssignmentSerializer
    permission_classes = [IsAdmin]

class StudentEnrollmentListCreateView(generics.ListCreateAPIView):
    queryset = StudentEnrollment.objects.all()
    serializer_class = StudentEnrollmentSerializer
    permission_classes = [IsAdmin]

# Vues pour les enseignants
class TeacherClassAssignmentListView(generics.ListAPIView):
    serializer_class = ClassAssignmentSerializer
    permission_classes = [IsTeacher]
    
    def get_queryset(self):
        return ClassAssignment.objects.filter(teacher=self.request.user)

class TeacherGradeListCreateView(generics.ListCreateAPIView):
    serializer_class = GradeSerializer
    permission_classes = [IsTeacher]
    
    def get_queryset(self):
        teacher_assignments = ClassAssignment.objects.filter(teacher=self.request.user)
        classes = teacher_assignments.values_list('class_obj', flat=True)
        subjects = teacher_assignments.values_list('subject', flat=True)
        
        return Grade.objects.filter(
            class_obj__in=classes,
            subject__in=subjects
        )
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class TeacherAttendanceListCreateView(generics.ListCreateAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [IsTeacher]
    
    def get_queryset(self):
        teacher_assignments = ClassAssignment.objects.filter(teacher=self.request.user)
        classes = teacher_assignments.values_list('class_obj', flat=True)
        
        return Attendance.objects.filter(class_obj__in=classes)
    
    def perform_create(self, serializer):
        serializer.save(recorded_by=self.request.user)

@api_view(['GET'])
@permission_classes([IsTeacher])
def teacher_dashboard_stats(request):
    teacher_assignments = ClassAssignment.objects.filter(teacher=request.user)
    classes_count = teacher_assignments.values('class_obj').distinct().count()
    subjects_count = teacher_assignments.values('subject').distinct().count()
    
    class_ids = teacher_assignments.values_list('class_obj', flat=True)
    students_count = StudentEnrollment.objects.filter(class_obj__in=class_ids).count()
    
    return Response({
        'classes_count': classes_count,
        'subjects_count': subjects_count,
        'students_count': students_count,
    })