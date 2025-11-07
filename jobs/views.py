from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from django.db import IntegrityError, models
from .models import JobPosting, Application
from .recommendations import get_recommended_jobs, get_recommended_applicants
from accounts.models import Recruiter, Applicant, Project
from accounts.decorators import recruiter_required, applicant_required

# Create your views here.
def index(request):
    # Get filter parameters
    search_term = request.GET.get('search')
    work_type = request.GET.get('work_type')
    location = request.GET.get('location')
    salary_min = request.GET.get('salary_min')
    salary_max = request.GET.get('salary_max')
    visa_sponsorship = request.GET.get('visa_sponsorship')
    my_jobs = request.GET.get('my_jobs')  # Filter for recruiter's own jobs
    skills_search = request.GET.get('skills_search')
    location_search = request.GET.get('location_search')
    
    # Start with base queryset
    job_postings = JobPosting.objects.filter(is_draft=False, is_closed=False)
    
    # Apply search filter
    if search_term:
        job_postings = job_postings.filter(
            models.Q(title__icontains=search_term) |
            models.Q(recruiter__company_name__icontains=search_term) |
            models.Q(skills_required__icontains=search_term)
        )
    
    # Apply skills search filter (new search bar)
    if skills_search:
        # Support comma-separated skills
        skills_list = [skill.strip() for skill in skills_search.split(',') if skill.strip()]
        for skill in skills_list:
            job_postings = job_postings.filter(skills_required__icontains=skill)
    
    # Apply location search filter (new search bar)
    if location_search:
        job_postings = job_postings.filter(location__icontains=location_search)
    
    # Apply work type filter
    if work_type == 'remote':
        job_postings = job_postings.filter(remote=True)
    elif work_type == 'onsite':
        job_postings = job_postings.filter(remote=False)
    elif work_type == 'hybrid':
        # For hybrid, we'll show both remote and onsite jobs
        pass  # No additional filtering needed
    
    # Apply specific location filter (for onsite/hybrid jobs)
    if location and work_type in ['onsite', 'hybrid']:
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
        'work_type': work_type,
        'location': location,
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
    
    # Prevent recruiters from applying to their own jobs
    if hasattr(request.user, 'recruiter') and listing.recruiter == request.user.recruiter:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.headers.get('Accept') == 'application/json':
            return JsonResponse({
                'success': False,
                'error': 'You cannot apply to your own job posting.'
            }, status=400)
        return HttpResponseBadRequest("You cannot apply to your own job posting.")
    
    note = request.POST.get('note', '')
    
    # Check if the applicant has already applied to this job
    existing_application = Application.objects.filter(
        applicant=applicant,
        listing=listing
    ).first()
    
    if existing_application:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.headers.get('Accept') == 'application/json':
            return JsonResponse({
                'success': False,
                'error': 'You have already applied to this job.'
            }, status=400)
        return HttpResponseBadRequest("You have already applied to this job.")
    
    # Create new application
    try:
        application = Application.objects.create(
            applicant=applicant,
            listing=listing,
            message=note
        )
    except IntegrityError:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.headers.get('Accept') == 'application/json':
            return JsonResponse({
                'success': False,
                'error': 'You have already applied to this job.'
            }, status=400)
        return HttpResponseBadRequest("You have already applied to this job.")

    # Always return JSON for AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.headers.get('Accept') == 'application/json':
        return JsonResponse({
            'success': True,
            'id': application.id,
            'listing_id': listing.id,
            'message': application.message,
        }, status=200)
    return redirect('jobs:jobs.index')


@recruiter_required
def recruiter_jobs(request):
    recruiter = request.user.recruiter
    jobs = JobPosting.objects.filter(recruiter=recruiter).order_by('-created_at')
    return render(request, 'jobs/recruiter_jobs.html', {'jobs': jobs})


@recruiter_required
@require_http_methods(["GET", "POST"])
def recruiter_job_new(request):
    recruiter = request.user.recruiter
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        skills_required = request.POST.get('skills', '').strip()
        location = request.POST.get('location-value', '').strip()
        salary_min = request.POST.get('salary_min') or 0
        salary_max = request.POST.get('salary_max') or 0
        work_type = request.POST.get('work_type')
        visa_sponsorship = bool(request.POST.get('visa_sponsorship'))
        save_as_draft = bool(request.POST.get('save_draft'))
        

        # Get address fields
        street_address = request.POST.get('street_address', '').strip()
        post_code = request.POST.get('post_code', '').strip()
        city = request.POST.get('city', '').strip()
        state = request.POST.get('state', '').strip()
        country = request.POST.get('country', 'USA').strip()
        
        if not title or not description or not street_address or not city or not state:
            return HttpResponseBadRequest("Missing required fields: title, description, street_address, city, and state are required.")

        job = JobPosting.objects.create(
            title=title,
            description=description,
            skills_required=skills_required,
            location=location,  # Keep for backward compatibility
            street_address=street_address,
            post_code=post_code,
            city=city,
            state=state,
            country=country,
            salary_min=salary_min,
            salary_max=salary_max,
            remote=(work_type == 'remote'),
            visa_sponsorship=visa_sponsorship,
            recruiter=recruiter,
            is_draft=save_as_draft,
        )
        return redirect('jobs:jobs.recruiter_jobs')

    return render(request, 'jobs/recruiter_job_new.html')


@recruiter_required
@require_http_methods(["GET", "POST"])
def recruiter_job_edit(request, job_id):
    recruiter = request.user.recruiter
    job = get_object_or_404(JobPosting, pk=job_id, recruiter=recruiter)

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        skills_required = request.POST.get('skills', '').strip()
        location = request.POST.get('location-value', '').strip()
        salary_min = request.POST.get('salary_min') or job.salary_min
        salary_max = request.POST.get('salary_max') or job.salary_max
        work_type = request.POST.get('work_type')
        visa_sponsorship = bool(request.POST.get('visa_sponsorship'))
        save_as_draft = bool(request.POST.get('save_draft'))

        # Get address fields
        street_address = request.POST.get('street_address', '').strip()
        post_code = request.POST.get('post_code', '').strip()
        city = request.POST.get('city', '').strip()
        state = request.POST.get('state', '').strip()
        country = request.POST.get('country', 'USA').strip()
        
        if not title or not description or not street_address or not city or not state:
            return HttpResponseBadRequest("Missing required fields: title, description, street_address, city, and state are required.")

        job.title = title
        job.description = description
        job.skills_required = skills_required
        job.location = location  # Keep for backward compatibility
        job.street_address = street_address
        job.post_code = post_code
        job.city = city
        job.state = state
        job.country = country
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
    job.is_closed = True
    job.save()
    return redirect('jobs:jobs.recruiter_jobs')


@recruiter_required
@require_http_methods(["POST"])
def reopen_job(request, job_id):
    recruiter = request.user.recruiter
    job = get_object_or_404(JobPosting, pk=job_id, recruiter=recruiter)
    job.is_closed = False
    job.save()
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
        applicant.phone = request.POST.get('phone', '').strip()
        applicant.location = request.POST.get('location-value', '').strip() or request.POST.get('location', '').strip()
        applicant.availability = request.POST.get('availability', 'open-to-work')
        applicant.save()
        return redirect('home:profile_edit')
    
    return render(request, 'accounts/profile_edit.html', {'applicant': applicant})

def my_applications(request):
    if request.user.is_authenticated and hasattr(request.user, 'applicant'):
        # Authenticated user with applicant profile
        applicant = request.user.applicant
        applications = Application.objects.filter(applicant=applicant).select_related('listing', 'listing__recruiter').order_by('-created_at')
        
        # If no real applications, show demo data
        if not applications.exists():
            applications = get_demo_applications()
    else:
        # Demo data for non-authenticated users or users without applicant profile
        applications = get_demo_applications()
    
    template_data = {
        'title': 'My Applications',
        'applications': applications
    }
    return render(request, 'jobs/my_applications.html', {'template_data': template_data})

def get_demo_applications():
    """Return demo application data for testing purposes"""
    class DemoApplication:
        def __init__(self, id, status, company_name, title, location, remote, created_at, message):
            self.id = id
            self.status = status
            self.created_at = created_at
            self.message = message
            self.listing = DemoJobListing(company_name, title, location, remote)
    
    class DemoJobListing:
        def __init__(self, company_name, title, location, remote):
            self.title = title
            self.location = location
            self.remote = remote
            self.recruiter = DemoRecruiter(company_name)
    
    class DemoRecruiter:
        def __init__(self, company_name):
            self.company_name = company_name
    
    return [
        DemoApplication(1, "Applied", "Google", "Software Engineer", "New York City, NY", True, "2024-01-15", "Excited about this opportunity!"),
        DemoApplication(2, "Closed", "Microsoft", "Product Manager", "Seattle, WA", False, "2024-01-10", "Thank you for considering my application."),
        DemoApplication(3, "Interviewing", "Apple", "iOS Developer", "Cupertino, CA", False, "2024-01-08", "Looking forward to discussing this role."),
        DemoApplication(4, "Review", "Meta", "Frontend Developer", "Menlo Park, CA", True, "2024-01-05", "Passionate about React and modern web development."),
        DemoApplication(5, "Offer", "Netflix", "Backend Engineer", "Los Gatos, CA", True, "2024-01-03", "Thrilled about the possibility of joining Netflix!"),
    ]


@recruiter_required
def job_applications(request, job_id):
    """View applications for a specific job posting"""
    recruiter = request.user.recruiter
    job = get_object_or_404(JobPosting, pk=job_id, recruiter=recruiter)
    applications = Application.objects.filter(listing=job).select_related('applicant', 'applicant__user').order_by('-id')
    
    
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