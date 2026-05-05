from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta

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
    # description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class Sprint(models.Model):
    DURATION_CHOICES = [
        (1, '1 Week (1w)'),
        (2, '2 Weeks (2w)'),
        (3, '3 Weeks (3w)'),
    ]
    name = models.CharField(max_length=255)
    goal = models.CharField(max_length=255)
    duration = models.IntegerField(choices=DURATION_CHOICES,default=2)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(blank=True,null=True)
    
    def save(self,*args, **kwargs):
        if not self.end_date and self.start_date:
            self.end_date = self.start_date + timedelta(weeks=self.duration)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name
    
class Task(models.Model):
    ISSUE_TYPE = [
        ('T','Task'),
        ('S','Story'),
        ('B','Bug')
    ]
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
    project = models.ForeignKey(Project,on_delete=models.CASCADE,related_name='tasks')
    issue_type = models.CharField(max_length=20,choices=ISSUE_TYPE,default="T")
    summary = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=10,choices=PRIORITY_CHOICES,default='M')
    attachment = models.ImageField(upload_to='project/',blank=True,null=True)
    assignee = models.ForeignKey(User,on_delete=models.SET_NULL,related_name='tasks',null=True,blank=True)
    sprint = models.ForeignKey(Sprint,on_delete=models.SET_NULL,null=True,blank=True,related_name='tasks')
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='TODO')
    due_date = models.DateTimeField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reporter = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name='reported_tasks')
    
    def __str__(self):
        return self.summary
    
