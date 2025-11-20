from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User, Role
from .serializers import UserSerializer, UserCreateSerializer, UserLoginSerializer, RoleSerializer
from .permissions import IsAdmin, IsOwnerOrAdmin

@api_view(['POST'])
def login_view(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            user_data = UserSerializer(user).data
            
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': user_data
            })
        
        return Response(
            {'error': 'Identifiants invalides'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAdmin]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserSerializer
    
    def get_queryset(self):
        queryset = User.objects.all()
        role = self.request.query_params.get('role')
        if role:
            queryset = queryset.filter(roles__name=role)
        return queryset

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrAdmin]

class RoleListView(generics.ListAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAdmin]

@api_view(['GET'])
@permission_classes([IsAdmin])
def admin_dashboard_stats(request):
    total_users = User.objects.count()
    total_teachers = User.objects.filter(roles__name='TEACHER').count()
    total_students = User.objects.filter(roles__name='STUDENT').count()
    
    return Response({
        'total_users': total_users,
        'total_teachers': total_teachers,
        'total_students': total_students,
    })