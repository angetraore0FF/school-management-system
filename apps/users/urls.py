from django.urls import path
from .views import (
    UserListCreateView, 
    UserDetailView, 
    RoleListView,
)

urlpatterns = [
    path('', UserListCreateView.as_view(), name='user-list-create'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('roles/', RoleListView.as_view(), name='role-list'),
]