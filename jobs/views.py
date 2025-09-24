from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from django.db import IntegrityError, models
from .models import JobPosting, Application
from accounts.models import Recruiter, Applicant, Project
from accounts.decorators import recruiter_required, applicant_required

# Create your views here.
def index(request):
    # Get filter parameters
    search_term = request.GET.get('search')
    location = request.GET.get('location')
    salary_min = request.GET.get('salary_min')
    salary_max = request.GET.get('salary_max')
    visa_sponsorship = request.GET.get('visa_sponsorship')
    my_jobs = request.GET.get('my_jobs')  # Filter for recruiter's own jobs
    
    # Start with base queryset
    job_postings = JobPosting.objects.filter(is_draft=False, is_closed=False)
    
    # Apply search filter
    if search_term:
        job_postings = job_postings.filter(
            models.Q(title__icontains=search_term) |
            models.Q(recruiter__company_name__icontains=search_term) |
            models.Q(skills_required__icontains=search_term)
        )
    
    # Apply location filter
    if location == 'remote':
        job_postings = job_postings.filter(remote=True)
    elif location == 'onsite':
        job_postings = job_postings.filter(remote=False)
    
    # Apply salary filters
    if salary_min:
        try:
            job_postings = job_postings.filter(salary_max__gte=float(salary_min))
        except ValueError:
            pass
    
    if salary_max:
        try:
            job_postings = job_postings.filter(salary_min__lte=float(salary_max))
        except ValueError:
            pass
    
    # Apply visa sponsorship filter
    if visa_sponsorship == 'true':
        job_postings = job_postings.filter(visa_sponsorship=True)
    
    # Show different content based on user type
    user_type = None
    applied_job_ids = []
    
    if request.user.is_authenticated:
        if hasattr(request.user, 'applicant'):
            user_type = 'applicant'
            # Get list of job IDs the user has already applied to
            applied_job_ids = list(Application.objects.filter(
                applicant=request.user.applicant,
                listing__in=job_postings
            ).values_list('listing_id', flat=True))
        elif hasattr(request.user, 'recruiter'):
            user_type = 'recruiter'
            # Apply "my jobs" filter for recruiters
            if my_jobs == 'true':
                job_postings = job_postings.filter(recruiter=request.user.recruiter)
    
    template_data = {
        'title': 'HireMap - Jobs',
        'job_postings': job_postings,
        'user_type': user_type,
        'search_term': search_term,
        'applied_job_ids': applied_job_ids,
        'my_jobs': my_jobs == 'true' if my_jobs else False
    }
    return render(request, 'jobs/index.html', {'template_data': template_data})


@login_required
def detail(request, job_id):
    job = get_object_or_404(JobPosting, id=job_id, is_draft=False, is_closed=False)
    
    # Split skills for template display
    skills_list = []
    if job.skills_required:
        skills_list = [skill.strip() for skill in job.skills_required.split(',') if skill.strip()]

    if request.method == "POST":
        if not hasattr(request.user, 'applicant'):
            return HttpResponseForbidden("Only applicants can apply to jobs.")
        # Get the logged-in user's applicant profile
        print("post request received")
        message = request.POST.get("message", "")
        applicant = get_object_or_404(Applicant, user=request.user)
        try:
            Application.objects.create(
                applicant=applicant,
                listing=job,
                message=message,
            )
        except IntegrityError:
            # Check if user has already applied to this job
            existing_application = Application.objects.filter(applicant=applicant, listing=job).first()
            if existing_application:
                return render(request, "jobs/job_detail.html", {
                    "title": f"HireMap - {job.title}",
                    "job": job,
                    "skills_list": skills_list,
                    "already_applied": True,
                    "existing_application": existing_application
                })
            else:
                return HttpResponseBadRequest("You have already applied to this job.")

        return redirect("jobs:jobs.detail", job_id=job.id)
    
    template_data = {
        "title": f"HireMap - {job.title}",
        "job": job,
        "skills_list": skills_list
    }
    return render(request, "jobs/job_detail.html", {
        "title": f"HireMap - {job.title}",
        "job": job,
        "skills_list": skills_list
    })


@login_required
@require_http_methods(["POST"])
def apply_to_job(request, job_id):
    if not hasattr(request.user, 'applicant'):
        return HttpResponseForbidden("Only applicants can apply to jobs.")
    applicant = request.user.applicant
    listing = get_object_or_404(JobPosting, pk=job_id, is_draft=False, is_closed=False)
    note = request.POST.get('note', '')
    try:
        application, created = Application.objects.get_or_create(
            applicant=applicant,
            listing=listing,
            defaults={'message': note}
        )
        if not created and note and application.message != note:
            application.message = note
            application.save(update_fields=['message'])
    except IntegrityError:
        return HttpResponseBadRequest("You have already applied to this job.")

    if request.headers.get('Accept') == 'application/json' or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'id': application.id,
            'listing_id': listing.id,
            'message': application.message,
        }, status=201)
    return redirect('jobs:jobs.index')


@recruiter_required
def recruiter_jobs(request):
    recruiter = request.user.recruiter
    jobs = JobPosting.objects.filter(recruiter=recruiter).order_by('-created_at')
    print(f"Recruiter: {recruiter.user.username}")
    print(f"Jobs found: {jobs.count()}")
    for job in jobs:
        print(f"  Job {job.id}: {job.title}")
    return render(request, 'jobs/recruiter_jobs.html', {'jobs': jobs})


@recruiter_required
@require_http_methods(["GET", "POST"])
def recruiter_job_new(request):
    recruiter = request.user.recruiter
    if request.method == 'POST':
        print("POST data received:", dict(request.POST))
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        skills_required = request.POST.get('skills', '').strip()
        location = request.POST.get('location', '').strip()
        salary_min = request.POST.get('salary_min') or 0
        salary_max = request.POST.get('salary_max') or 0
        work_type = request.POST.get('work_type')
        visa_sponsorship = bool(request.POST.get('visa_sponsorship'))
        save_as_draft = bool(request.POST.get('save_draft'))
        
        print(f"Title: {title}, Description: {description}, Location: {location}")
        print(f"Save as draft: {save_as_draft}")

        if not title or not description or not location:
            return HttpResponseBadRequest("Missing required fields.")

        job = JobPosting.objects.create(
            title=title,
            description=description,
            skills_required=skills_required,
            location=location,
            salary_min=salary_min,
            salary_max=salary_max,
            remote=(work_type == 'remote'),
            visa_sponsorship=visa_sponsorship,
            recruiter=recruiter,
            is_draft=save_as_draft,
        )
        print(f"Job created: {job.id}, Draft: {job.is_draft}")
        return redirect('jobs:jobs.recruiter_jobs')

    return render(request, 'jobs/recruiter_job_new.html')


@recruiter_required
@require_http_methods(["GET", "POST"])
def recruiter_job_edit(request, job_id):
    recruiter = request.user.recruiter
    job = get_object_or_404(JobPosting, pk=job_id, recruiter=recruiter)
    print(f"Editing job {job_id} for recruiter {recruiter.user.username}")

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        skills_required = request.POST.get('skills', '').strip()
        location = request.POST.get('location', '').strip()
        salary_min = request.POST.get('salary_min') or job.salary_min
        salary_max = request.POST.get('salary_max') or job.salary_max
        work_type = request.POST.get('work_type')
        visa_sponsorship = bool(request.POST.get('visa_sponsorship'))
        save_as_draft = bool(request.POST.get('save_draft'))

        if not title or not description or not location:
            return HttpResponseBadRequest("Missing required fields.")

        job.title = title
        job.description = description
        job.skills_required = skills_required
        job.location = location
        job.salary_min = salary_min
        job.salary_max = salary_max
        job.remote = (work_type == 'remote') if work_type is not None else job.remote
        job.visa_sponsorship = visa_sponsorship
        job.is_draft = save_as_draft
        job.save()
        return redirect('jobs:jobs.recruiter_jobs')

    initial = {
        'job': job,
    }
    return render(request, 'jobs/recruiter_job_new.html', initial)


@recruiter_required
@require_http_methods(["POST"])
def close_job(request, job_id):
    recruiter = request.user.recruiter
    job = get_object_or_404(JobPosting, pk=job_id, recruiter=recruiter)
    print(f"Closing job {job_id} for recruiter {recruiter.user.username}")
    job.is_closed = True
    job.save()
    print(f"Job {job_id} closed successfully")
    return redirect('jobs:jobs.recruiter_jobs')


@recruiter_required
@require_http_methods(["POST"])
def reopen_job(request, job_id):
    recruiter = request.user.recruiter
    job = get_object_or_404(JobPosting, pk=job_id, recruiter=recruiter)
    print(f"Reopening job {job_id} for recruiter {recruiter.user.username}")
    job.is_closed = False
    job.save()
    print(f"Job {job_id} reopened successfully")
    return redirect('jobs:jobs.recruiter_jobs')


@recruiter_required
def view_applicant_profile(request, applicant_id):
    recruiter = request.user.recruiter
    applicant = get_object_or_404(Applicant, pk=applicant_id)
    return render(request, 'accounts/applicant_profile.html', {'applicant': applicant})


@applicant_required
@require_http_methods(["GET", "POST"])
def edit_profile(request):
    applicant = request.user.applicant
    if request.method == 'POST':
        applicant.first_name = request.POST.get('first_name', '').strip()
        applicant.last_name = request.POST.get('last_name', '').strip()
        applicant.skills = request.POST.get('skills', '').strip()
        applicant.education = request.POST.get('education', '').strip()
        applicant.experience = request.POST.get('experience', '').strip()
        applicant.projects = request.POST.get('projects', '').strip()
        applicant.links = request.POST.get('links', '').strip()
        applicant.save()
        return redirect('home:profile_edit')
    
    return render(request, 'accounts/profile_edit.html', {'applicant': applicant})

@applicant_required
def my_applications(request):
    applicant = request.user.applicant
    applications = Application.objects.filter(applicant=applicant).select_related('listing', 'listing__recruiter').order_by('-id')
    
    template_data = {
        'title': 'My Applications',
        'applications': applications
    }
    return render(request, 'jobs/my_applications.html', {'template_data': template_data})


@recruiter_required
def job_applications(request, job_id):
    """View applications for a specific job posting"""
    recruiter = request.user.recruiter
    job = get_object_or_404(JobPosting, pk=job_id, recruiter=recruiter)
    applications = Application.objects.filter(listing=job).select_related('applicant', 'applicant__user').order_by('-id')
    
    # Debug: Print application data
    print(f"Job {job_id} applications: {applications.count()}")
    for app in applications:
        print(f"  Application {app.id}: applicant_user_id={app.applicant.user.id if app.applicant else 'None'}, applicant={app.applicant}")
    
    template_data = {
        'title': f'Applications for {job.title}',
        'job': job,
        'applications': applications
    }
    return render(request, 'jobs/job_applications.html', {'template_data': template_data})


@applicant_required
@require_http_methods(["GET", "POST"])
def manage_projects(request):
    """View and manage applicant projects"""
    applicant = request.user.applicant
    projects = Project.objects.filter(applicant=applicant)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add':
            title = request.POST.get('title', '').strip()
            description = request.POST.get('description', '').strip()
            technologies = request.POST.get('technologies', '').strip()
            url = request.POST.get('url', '').strip()
            
            if title and description:
                Project.objects.create(
                    applicant=applicant,
                    title=title,
                    description=description,
                    technologies=technologies,
                    url=url
                )
        
        elif action == 'delete':
            project_id = request.POST.get('project_id')
            if project_id:
                try:
                    project = Project.objects.get(id=project_id, applicant=applicant)
                    project.delete()
                except Project.DoesNotExist:
                    pass
        
        return redirect('jobs:jobs.manage_projects')
    
    template_data = {
        'title': 'My Projects',
        'projects': projects
    }
    return render(request, 'jobs/manage_projects.html', {'template_data': template_data})