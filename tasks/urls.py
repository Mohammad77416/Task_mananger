from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet , ProjectViewSet , TaskViewSet , RegisterView,UserListView,SprintViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'users', UserViewSet, basename='user')
router.register(r'sprint',SprintViewSet,basename='sprint')
router.register(r'register',RegisterView,basename='register')

urlpatterns = [
    path('', include(router.urls)),
    # path('register/',RegisterView.as_view(),name='register'),
    path('users/',UserListView.as_view(),name='user-list'),
]