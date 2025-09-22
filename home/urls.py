from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home.index'),
    # SPA deep-links that should render the same index.html shell:
    path('jobs/', views.index, name='jobs.list'),
    path('jobs/<int:pk>/', views.index, name='jobs.detail'),
    path('applications/', views.index, name='applications.board'),
    path('profile/', views.index, name='profile.edit'),
    path('recruiter/jobs/', views.index, name='recruiter.jobs'),
    path('recruiter/jobs/new/', views.index, name='recruiter.jobs.new'),
    path('messages/', views.index, name='messages.inbox'),
    path('map/', views.index, name='map'),
]
