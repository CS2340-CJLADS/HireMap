from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'accounts.index'),
    path('signup', views.recruiter_signup, name = 'accounts.recruiter_signup'),
    path('login', views.login, name = 'accounts.login'),
    path('logout', views.logout, name = 'accounts.logout')
]