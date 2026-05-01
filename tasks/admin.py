from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User , Project , Task
# Register your models here.

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('اطلاعات نقش',{'fields':('role',)}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('اطلاعات نقش',{'fields':('role',)}),
    )
    
    list_display = ('username','email','role','is_staff')

admin.site.register(User,CustomUserAdmin)
admin.site.register(Project)
admin.site.register(Task)
