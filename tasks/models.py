from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN','ادمین سیستم'),
        ('Mananger','مدیر سیستم'),
        ('MEMBER','عضو عادی'),
    )
    role = models.CharField(max_length=10,choices=ROLE_CHOICES,default='MEMBER',verbose_name='نقش کاربری')
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class Task(models.Model):
    PRIORITY_CHOICES = [
        ('L','LOW'),
        ('M','MEDIUM'),
        ('H','HIGH'),
    ]
    
    STATUS_CHOICES = [
        ('TODO','To Do'),
        ('IN_PROGRESS','In Progress'),
        ('DONE','Done'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='TODO')
    priority = models.CharField(max_length=10,choices=PRIORITY_CHOICES,default='M')
    due_date = models.DateTimeField(null=True,blank=True)
    project = models.ForeignKey(Project,on_delete=models.CASCADE,related_name='tasks')
    assignee = models.ForeignKey(User,on_delete=models.CASCADE,related_name='assignee')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
