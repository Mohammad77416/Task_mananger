from django.shortcuts import render
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .models import User,Project,Task
from .serializers import UserSerializer,ProjectSerializer,TaskSerializer
# Create your views here.
User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend , SearchFilter , OrderingFilter]
    filterset_fields = ['status', 'priority', 'project', 'assignee']
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'created_at', 'priority']
    ordering = ['-created_at']
