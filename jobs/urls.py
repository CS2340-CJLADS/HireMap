from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'jobs.index'),
    path("<int:job_id>/", views.detail, name="jobs.detail"),
    path('<int:job_id>/apply/', views.apply_to_job, name='jobs.apply'),
    path('recruiter/jobs/', views.recruiter_jobs, name='jobs.recruiter_jobs'),
    path('recruiter/jobs/new/', views.recruiter_job_new, name='jobs.recruiter_job_new'),
    path('recruiter/jobs/<int:job_id>/edit/', views.recruiter_job_edit, name='jobs.recruiter_job_edit'),
    path('recruiter/jobs/<int:job_id>/close/', views.close_job, name='jobs.close_job'),
    path('recruiter/jobs/<int:job_id>/reopen/', views.reopen_job, name='jobs.reopen_job'),
    path('recruiter/jobs/<int:job_id>/applications/', views.job_applications, name='jobs.job_applications'),
    path('applicant/<int:applicant_id>/profile/', views.view_applicant_profile, name='jobs.view_applicant_profile'),
    path('profile/edit/', views.edit_profile, name='jobs.edit_profile'),
    path('my-applications/', views.my_applications, name='jobs.my_applications'),
    path('projects/', views.manage_projects, name='jobs.manage_projects'),
]