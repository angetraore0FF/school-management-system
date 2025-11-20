from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

from apps.users.models import User
from apps.academic.models import ClassAssignment, Grade, Attendance, SchoolYear, Class, Subject
from apps.users.serializers import UserLoginSerializer, UserSerializer
from .serializers import DashboardStatsSerializer, TeacherDashboardSerializer, LoginResponseSerializer
from .permissions import HasRole

@api_view(['POST'])
def login_view(request):
    """
    Endpoint de connexion centralisé
    Retourne le token JWT et les informations de l'utilisateur
    """
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            user_data = UserSerializer(user).data
            
            # Déterminer l'URL du dashboard en fonction du rôle
            primary_role = user.get_primary_role()
            if primary_role == 'ADMIN':
                dashboard_url = '/admin-dashboard'
            elif primary_role == 'TEACHER':
                dashboard_url = '/teacher-portal'
            elif primary_role == 'STUDENT':
                dashboard_url = '/student-portal'
            elif primary_role == 'PARENT':
                dashboard_url = '/parent-portal'
            else:
                dashboard_url = '/'
            
            response_data = {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': user_data,
                'dashboard_url': dashboard_url
            }
            
            return Response(response_data)
        
        return Response(
            {'error': 'Identifiants invalides'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(generics.RetrieveAPIView):
    """
    Endpoint pour récupérer le profil de l'utilisateur connecté
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user

class DashboardView(generics.RetrieveAPIView):
    """
    Endpoint centralisé pour les données du dashboard
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        user = request.user
        primary_role = user.get_primary_role()
        
        if primary_role == 'ADMIN':
            return self.get_admin_dashboard(request)
        elif primary_role == 'TEACHER':
            return self.get_teacher_dashboard(request)
        elif primary_role == 'STUDENT':
            return self.get_student_dashboard(request)
        else:
            return Response(
                {'error': 'Dashboard non disponible pour votre rôle'},
                status=status.HTTP_403_FORBIDDEN
            )
    
    def get_admin_dashboard(self, request):
        from apps.users.models import User
        from apps.academic.models import SchoolYear, Class, Subject
        
        total_users = User.objects.count()
        total_teachers = User.objects.filter(roles__name='TEACHER').count()
        total_students = User.objects.filter(roles__name='STUDENT').count()
        total_classes = Class.objects.count()
        total_subjects = Subject.objects.count()
        active_school_year = SchoolYear.objects.filter(is_active=True).first()
        
        data = {
            'total_users': total_users,
            'total_teachers': total_teachers,
            'total_students': total_students,
            'total_classes': total_classes,
            'total_subjects': total_subjects,
            'active_school_year': active_school_year.name if active_school_year else None,
            'role': 'admin'
        }
        
        serializer = DashboardStatsSerializer(data)
        return Response(serializer.data)
    
    def get_teacher_dashboard(self, request):
        teacher_assignments = ClassAssignment.objects.filter(teacher=request.user)
        classes_count = teacher_assignments.values('class_obj').distinct().count()
        subjects_count = teacher_assignments.values('subject').distinct().count()
        
        class_ids = teacher_assignments.values_list('class_obj', flat=True)
        students_count = User.objects.filter(
            roles__name='STUDENT',
            studentenrollment__class_obj__in=class_ids
        ).distinct().count()
        
        # Compter les notes et absences récentes
        recent_grades = Grade.objects.filter(created_by=request.user).count()
        recent_attendances = Attendance.objects.filter(recorded_by=request.user).count()
        
        data = {
            'classes_count': classes_count,
            'subjects_count': subjects_count,
            'students_count': students_count,
            'recent_grades': recent_grades,
            'recent_attendances': recent_attendances,
            'role': 'teacher'
        }
        
        serializer = TeacherDashboardSerializer(data)
        return Response(serializer.data)
    
    def get_student_dashboard(self, request):
        # Placeholder pour le dashboard étudiant
        data = {
            'message': 'Dashboard étudiant en développement',
            'role': 'student'
        }
        return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated, HasRole('ADMIN')])
def system_health(request):
    """
    Endpoint pour vérifier la santé du système (Admin seulement)
    """
    from django.db import connection
    from django.core.cache import cache
    
    # Test de la base de données
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        db_status = 'OK'
    except Exception as e:
        db_status = f'ERROR: {str(e)}'
    
    # Test du cache
    try:
        cache.set('health_check', 'ok', 10)
        cache_status = 'OK' if cache.get('health_check') == 'ok' else 'ERROR'
    except Exception as e:
        cache_status = f'ERROR: {str(e)}'
    
    return Response({
        'database': db_status,
        'cache': cache_status,
        'status': 'healthy'
    })