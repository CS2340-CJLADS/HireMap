from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from accounts.decorators import recruiter_required
from accounts.models import Applicant
from jobs.models import JobPosting, Application

# Create your views here.

@login_required
@recruiter_required
def dashboard(request):
    """Recruiter dashboard"""
    recruiter = request.user.recruiter
    
    # Get filter parameters (same as seeker dashboard)
    search_term = request.GET.get('search')
    title = request.GET.get('title')
    location = request.GET.get('location')
    skills = request.GET.get('skills')
    salary_min = request.GET.get('salary_min')
    salary_max = request.GET.get('salary_max')
    visa_sponsorship = request.GET.get('visa_sponsorship')
    
    # Start with base queryset (all jobs, not just recruiter's)
    job_postings = JobPosting.objects.filter(is_draft=False, is_closed=False)
    
    # Apply search filter
    if search_term:
        job_postings = job_postings.filter(
            Q(title__icontains=search_term) |
            Q(recruiter__company_name__icontains=search_term) |
            Q(skills_required__icontains=search_term)
        )
    
    # Apply title filter
    if title:
        job_postings = job_postings.filter(title__icontains=title)
    
    # Apply skills filter
    if skills:
        job_postings = job_postings.filter(skills_required__icontains=skills)
    
    # Apply location filter
    if location:
        if location.lower() == 'remote':
            job_postings = job_postings.filter(remote=True)
        elif location.lower() == 'onsite' or location.lower() == 'on-site':
            job_postings = job_postings.filter(remote=False)
        else:
            # Search in location field for text matches
            job_postings = job_postings.filter(location__icontains=location)
    
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
    
    # Get recruiter's jobs
    jobs = JobPosting.objects.filter(recruiter=recruiter).order_by('-created_at')
    
    # Get recent applications (exclude those with missing applicant IDs and self-applications)
    recent_applications = Application.objects.filter(
        listing__recruiter=recruiter,
        applicant__isnull=False
    ).exclude(
        applicant__user=recruiter.user  # Exclude applications where applicant is the same as recruiter
    ).select_related('applicant', 'listing').order_by('-created_at')[:10]
    
    
    template_data = {
        'title': 'Recruiter Dashboard',
        'recruiter': recruiter,
        'job_postings': job_postings,
        'jobs': jobs,
        'recent_applications': recent_applications,
        'total_jobs': jobs.count(),
        'total_applications': Application.objects.filter(listing__recruiter=recruiter).count(),
        'search_term': search_term,
    }
    
    return render(request, 'recruiter/dashboard.html', {'template_data': template_data})

@login_required
@recruiter_required
def profile(request):
    """View and edit recruiter profile"""
    recruiter = request.user.recruiter
    
    template_data = {
        'title': 'My Profile',
        'recruiter': recruiter
    }
    return render(request, 'accounts/recruiter_profile.html', {'template_data': template_data})

@login_required
@recruiter_required
def jobs(request):
    """Manage job postings"""
    recruiter = request.user.recruiter
    jobs = JobPosting.objects.filter(recruiter=recruiter).order_by('-created_at')
    
    template_data = {
        'title': 'Manage Jobs',
        'jobs': jobs,
    }
    return render(request, 'recruiter/jobs.html', {'template_data': template_data})

@login_required
@recruiter_required
def job_new(request):
    """Create new job posting"""
    recruiter = request.user.recruiter
    
    if request.method == 'POST':
        # Get the action (publish or draft)
        action = request.POST.get('action', 'publish')
        is_draft = action == 'draft'
        
        # Create new job posting
        job = JobPosting.objects.create(
            title=request.POST.get('title', ''),
            description=request.POST.get('description', ''),
            skills_required=request.POST.get('skills_required', ''),
            location=request.POST.get('location', ''),
            salary_min=float(request.POST.get('salary_min', 0)),
            salary_max=float(request.POST.get('salary_max', 0)),
            remote=request.POST.get('remote') == 'on',
            visa_sponsorship=request.POST.get('visa_sponsorship') == 'on',
            recruiter=recruiter,
            is_draft=is_draft,
        )
        return redirect('recruiter:jobs')
    
    template_data = {
        'title': 'Post New Job',
    }
    return render(request, 'recruiter/job_new.html', {'template_data': template_data})

@login_required
@recruiter_required
def job_edit(request, job_id):
    """Edit job posting"""
    recruiter = request.user.recruiter
    job = get_object_or_404(JobPosting, id=job_id, recruiter=recruiter)
    
    if request.method == 'POST':
        # Get the action (publish or draft)
        action = request.POST.get('action', 'publish')
        is_draft = action == 'draft'
        
        job.title = request.POST.get('title', '')
        job.description = request.POST.get('description', '')
        job.skills_required = request.POST.get('skills_required', '')
        job.location = request.POST.get('location', '')
        job.salary_min = float(request.POST.get('salary_min', 0))
        job.salary_max = float(request.POST.get('salary_max', 0))
        job.remote = request.POST.get('remote') == 'on'
        job.visa_sponsorship = request.POST.get('visa_sponsorship') == 'on'
        job.is_draft = is_draft
        job.save()
        return redirect('recruiter:jobs')
    
    template_data = {
        'title': 'Edit Job',
        'job': job,
    }
    return render(request, 'recruiter/job_edit.html', {'template_data': template_data})

@login_required
@recruiter_required
def job_applications(request, job_id):
    """View applications for a specific job"""
    recruiter = request.user.recruiter
    job = get_object_or_404(JobPosting, id=job_id, recruiter=recruiter)
    applications = Application.objects.filter(
        listing=job,
        applicant__isnull=False
    ).exclude(
        applicant__user=recruiter.user  # Exclude applications where applicant is the same as recruiter
    ).select_related('applicant').order_by('-created_at')
    
    template_data = {
        'title': f'Applications for {job.title}',
        'job': job,
        'applications': applications,
    }
    return render(request, 'recruiter/job_applications.html', {'template_data': template_data})

@login_required
@recruiter_required
def job_delete(request, job_id):
    """Delete job posting"""
    recruiter = request.user.recruiter
    job = get_object_or_404(JobPosting, id=job_id, recruiter=recruiter)
    
    if request.method == 'POST':
        job.delete()
        return redirect('recruiter:jobs')
    
    template_data = {
        'title': 'Delete Job',
        'job': job,
    }
    return render(request, 'recruiter/job_delete.html', {'template_data': template_data})

@login_required
@recruiter_required
def view_applicant(request, applicant_id):
    """View applicant profile"""
    recruiter = request.user.recruiter
    applicant = get_object_or_404(Applicant, pk=applicant_id)
    
    template_data = {
        'title': f'{applicant.first_name} {applicant.last_name}',
        'applicant': applicant,
    }
    return render(request, 'accounts/applicant_profile.html', {'template_data': template_data})