from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from .views import login_view, UserProfileView, DashboardView

urlpatterns = [
    # Authentication
    path('auth/login/', login_view, name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/profile/', UserProfileView.as_view(), name='user-profile'),
    
    # Dashboards
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    
    # Modules
    path('users/', include('apps.users.urls')),
    path('academic/', include('apps.academic.urls')),
    path('administration/', include('apps.administration.urls')),
]