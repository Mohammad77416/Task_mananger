from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Project,Task,Sprint,User

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['id','username','email','first_name','last_name','is_active']
        
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        
class TaskSerializer(serializers.ModelSerializer):
    # priority = serializers.CharField(write_only=True, required=False) 
    class Meta:
        model = Task
        # fields = '__all__'
        fields = ['id','summary', 'description', 'status', 'project', 'reporter', 'priority', 'created_at','attachment', 'issue_type', 'sprint', 'assignee','reporter'] 
        read_only_fields = ['reporter']
        extra_kwargs = {
            'priority': {'write_only': True, 'required': False}
        }
        
class SprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sprint
        fields = '__all__'
        
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = 'username' , 'password'
        
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user
    
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(help_text="send refresh token")
    
class PasswordResetRequestSerializer(serializers.Serializer):
    username = serializers.CharField()
    
class PasswordResetConfirmSerializer(serializers.Serializer):
    username = serializers.CharField()
    otp = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
