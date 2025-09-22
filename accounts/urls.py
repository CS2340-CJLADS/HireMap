from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'accounts.index'),
    path('RecruiterSignup', views.RecruiterSignup, name = 'accounts.RecruiterSignup')
    path('SeekerSignup', views.SeekerSignup, name = 'accounts.SeekerSignup')
    path('Login', views.login, name = 'accounts.login')
    path('Logout', views.logout, name = 'accounts.logout')
]