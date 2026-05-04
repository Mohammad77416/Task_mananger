from django.shortcuts import render
from rest_framework import viewsets , mixins
from rest_framework.views import APIView 
from rest_framework.decorators import action 
from rest_framework import generics , status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .models import User,Project,Task,Sprint
from .serializers import UserSerializer,ProjectSerializer,TaskSerializer,RegisterSerializer,SprintSerializer,LogoutSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema , inline_serializer
# Create your views here.
User = get_user_model()

@extend_schema(tags=['Users'])
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

@extend_schema(tags=['Projects'])
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

@extend_schema(tags=['Tasks'])
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [DjangoFilterBackend , SearchFilter , OrderingFilter]
    filterset_fields = ['status', 'priority', 'project', 'assignee']
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'created_at', 'priority']
    ordering = ['-created_at']
    
@extend_schema(tags=['Login'])
class RegisterView(mixins.CreateModelMixin,viewsets.GenericViewSet):
    queryset=User.objects.all()
    permission_classes=(AllowAny,)
    serializer_class=RegisterSerializer

    @action(detail=False,methods=['get'],permission_classes=[IsAuthenticated])
    def me(self,request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    @extend_schema(request=LogoutSerializer)
    @action(detail=False,methods=['post'],permission_classes=[IsAuthenticated])
    def logout(self,request):
        try:
            refresh_token  = request.data.get("refresh")
            if not refresh_token :
                return Response({"error" : "شما لاگین نیستید"},status=status.HTTP_406_NOT_ACCEPTABLE)
            
            token = RefreshToken(refresh_token )
            token.blacklist()
            return Response({"message":"با موفقیت خارج شدید"},status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error":"توکن نامعتبر است"},status=status.HTTP_400_BAD_REQUEST)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': serializer.data , 
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        },status=status.HTTP_201_CREATED)
        
    
        
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes=[IsAuthenticated]
   

@extend_schema(tags=['Sprints']) 
class SprintViewSet(viewsets.ModelViewSet):
    queryset = Sprint.objects.all()
    serializer_class = SprintSerializer
    permission_classes = [IsAuthenticated]
