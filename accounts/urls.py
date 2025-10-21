from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('signup/', views.signup, name = 'signup'),
    path('login/', views.login, name = 'login'),
    path('logout/', views.logout, name = 'logout'),
    path('api/locations/', views.get_locations, name = 'get_locations'),
    
    # Profile management
    path('profile/', views.profile_view, name = 'profile_view'),
    path('profile/<int:user_id>/', views.profile_view, name = 'profile_view'),
    path('profile/edit/', views.profile_edit, name = 'profile_edit'),
    path('recruiter/profile/edit/', views.recruiter_profile_edit, name = 'recruiter_profile_edit'),
    path('projects/', views.manage_projects, name = 'manage_projects'),
    
]