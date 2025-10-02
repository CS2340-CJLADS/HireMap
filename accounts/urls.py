from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'accounts.index'),
    path('signup/', views.signup, name = 'accounts.signup'),
    path('login/', views.login, name = 'accounts.login'),
    path('logout/', views.logout, name = 'accounts.logout'),
    path('api/locations/', views.get_locations, name = 'accounts.get_locations'),
]