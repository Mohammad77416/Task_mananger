from django.shortcuts import render
from rest_framework import viewsets , mixins , filters
from django_filters.rest_framework import DjangoFilterBackend
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
from .serializers import UserSerializer,ProjectSerializer,TaskSerializer,RegisterSerializer,SprintSerializer,LogoutSerializer,PasswordResetConfirmSerializer,PasswordResetRequestSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema , inline_serializer
from django.core.cache import cache
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
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    search_fields = ['summary','description']
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    filterset_fields = ['status', 'project', 'assignee','reporter']
    ordering = ['-created_at']
    
    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)
        
    def list(self, request, *args, **kwargs):
        user_id = request.user.id
        query_string = request.META.get('Query_String','')
        cache_key = f'task_list_user_{user_id}_{query_string}'
        cache_data = cache.get(cache_key)
        if cache_data is not None:
            print("Fetching from redis cache ...")
            return Response(cache_data)
        print("Fetching from database ...")
        response = super().list(request,*args,**kwargs)
        
        cache.set(cache_key,response.data,900)
        
        return response
            
    
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
        
    @extend_schema(request=PasswordResetRequestSerializer)
    @action(detail=False,methods=['post'],permission_classes=[IsAuthenticated])
    def passwordReset(self,request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            try:
                user = User.objects.get(username=username)
                return Response({"message":"کد بازیابی با موفقیت ارسال شد"},status=status.HTTP_200_OK)
            except user.DoesNotExist:
                return Response({"message":"کد بازیابی در صورت وجو کاربر ارسال خواهد شد"},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(request=PasswordResetConfirmSerializer)
    @action(detail=False,methods=['post'],permission_classes=[IsAuthenticated])
    def passwordResetConfirms(self,request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            otp = serializer.validated_data['otp']
            new_password = serializer.data['new_password']
            try:
                user = User.objects.get(username=username)
                user.set_password(new_password)
                user.save()
                return Response({"message":"رمز عبور با موفقیت تغییر پیدا کرد"},status=status.HTTP_200_OK)
            except user.DoesNotExist:
                return Response({"error":"کاربر یافت نشد"},status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
            
    
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
