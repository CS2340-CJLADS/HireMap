from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from accounts.decorators import applicant_required
from accounts.models import Applicant, Project
from jobs.models import JobPosting, Application
from jobs.recommendations import get_recommended_jobs
from django.db.models import Q, Value, CharField
from django.db.models.functions import Concat

# Create your views here.

def dashboard(request):
    """Job search dashboard - No login required for testing"""
    
    # Get filter parameters
    search_term = request.GET.get('search')
    title = request.GET.get('title')
    work_type = request.GET.get('work_type')
    location = request.GET.get('location')
    skills = request.GET.get('skills')
    salary_min = request.GET.get('salary_min')
    salary_max = request.GET.get('salary_max')
    visa_sponsorship = request.GET.get('visa_sponsorship')
    
    # Start with base queryset
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
    
    # Apply work type filter (Remote / In-Person)
    if work_type == 'remote':
        job_postings = job_postings.filter(remote=True)
    elif work_type == 'in-person':
        job_postings = job_postings.filter(remote=False)
    
    # Apply location filter (only for non-remote jobs)
    if location:
        # Location filter only applies to in-person jobs
        # Location format is "City, State" from the dropdown
        if ', ' in location:
            city, state = location.split(', ', 1)
            job_postings = job_postings.filter(
                remote=False,
                city__iexact=city.strip(),
                state__iexact=state.strip()
            )
        else:
            # Fallback: try to match city or state
            job_postings = job_postings.filter(
                remote=False
            ).filter(
                Q(city__icontains=location) | Q(state__icontains=location)
            )
    
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
    
    # Get applied job IDs (only if user is logged in as applicant)
    applied_job_ids = []
    recent_applications = []
    total_applications = 0
    total_projects = 0
    
    if request.user.is_authenticated and hasattr(request.user, 'applicant'):
        applicant = request.user.applicant
        applied_job_ids = list(Application.objects.filter(
            applicant=applicant,
            listing__in=job_postings
        ).values_list('listing_id', flat=True))
        
        # Get recent applications for dashboard
        recent_applications = Application.objects.filter(
            applicant=applicant
        ).select_related('listing', 'listing__recruiter').order_by('-created_at')[:5]
        
        # Get stats
        total_applications = Application.objects.filter(applicant=applicant).count()
        total_projects = Project.objects.filter(applicant=applicant).count()
        
        # Get recommended jobs for the applicant
        recommended_jobs = get_recommended_jobs(applicant, limit=5)
    else:
        recommended_jobs = []
    
    # Add pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(job_postings, 20)  # Show 20 jobs per page
    job_postings_page = paginator.get_page(page)
    
    # Get unique locations from actual job postings (all published, non-closed jobs)
    # Use city and state from address fields
    # Include both remote and in-person jobs to show all available locations
    all_jobs = JobPosting.objects.filter(
        is_draft=False, 
        is_closed=False
    ).exclude(city__isnull=True).exclude(city='').exclude(state__isnull=True).exclude(state='')
    
    # Build location strings in "City, State" format
    all_locations_list = []
    seen_locations = set()
    
    # Filter out invalid/spam locations
    invalid_locations = {'spam', 'SPAM', 'test', 'TEST', 'test location', 'example'}
    
    for job in all_jobs:
        if job.city and job.state:
            location_str = f"{job.city}, {job.state}"
            # Check if location is valid and not already seen
            if location_str not in seen_locations and location_str.lower() not in invalid_locations:
                all_locations_list.append(location_str)
                seen_locations.add(location_str)
    
    all_locations_list = sorted(all_locations_list)
    
    template_data = {
        'title': 'Job Search Dashboard',
        'job_postings': job_postings_page,
        'search_term': search_term,
        'applied_job_ids': applied_job_ids,
        'recent_applications': recent_applications,
        'total_applications': total_applications,
        'total_projects': total_projects,
        'recommended_jobs': recommended_jobs,
        'user_is_applicant': request.user.is_authenticated and hasattr(request.user, 'applicant'),
        'paginator': paginator,
        'current_page': page,
        'non_remote_locations': all_locations_list,
    }
    
    return render(request, 'seeker/dashboard.html', {'template_data': template_data})

@login_required
@applicant_required
def profile(request):
    """View and edit applicant profile"""
    applicant = request.user.applicant
    projects = Project.objects.filter(applicant=applicant)
    
    template_data = {
        'title': 'My Profile',
        'applicant': applicant,
        'projects': projects
    }
    return render(request, 'seeker/profile.html', {'template_data': template_data})

def applications(request):
    """View user's job applications - No login required for testing"""
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
    return render(request, 'seeker/applications.html', {'template_data': template_data})

def saved_jobs(request):
    """View saved jobs - placeholder for future implementation"""
    template_data = {
        'title': 'Saved Jobs',
    }
    return render(request, 'seeker/saved_jobs.html', {'template_data': template_data})

def get_demo_applications():
    """Return demo application data for testing purposes"""
    from django.contrib.auth.models import User
    from accounts.models import Applicant, Recruiter
    from jobs.models import JobPosting, Application
    
    # Create demo data if it doesn't exist
    demo_user, created = User.objects.get_or_create(
        username='demo@example.com',
        defaults={'email': 'demo@example.com'}
    )
    
    demo_applicant, created = Applicant.objects.get_or_create(
        user=demo_user,
        defaults={
            'first_name': 'Demo',
            'last_name': 'User',
            'phone': '555-0123',
            'location': 'San Francisco, CA',
            'skills': 'Python, JavaScript, React',
            'education': 'Computer Science, Stanford University',
            'experience': '3 years software development'
        }
    )
    
    demo_recruiter, created = Recruiter.objects.get_or_create(
        user=demo_user,
        defaults={
            'first_name': 'Demo',
            'last_name': 'Recruiter',
            'company_name': 'Google',
            'location': 'Mountain View, CA'
        }
    )
    
    # Create demo job postings
    demo_job1, created = JobPosting.objects.get_or_create(
        title='Software Engineer Intern',
        recruiter=demo_recruiter,
        defaults={
            'description': 'We are looking for a Software Engineer to design, develop, and maintain scalable applications.',
            'location': 'New York City, NY',
            'remote': True,
            'salary_min': 70000,
            'salary_max': 100000,
            'skills_required': 'Python, Java, Git, GitHub',
            'visa_sponsorship': True,
            'is_draft': False,
            'is_closed': False
        }
    )
    
    # Create demo applications
    demo_app1, created = Application.objects.get_or_create(
        applicant=demo_applicant,
        listing=demo_job1,
        defaults={
            'message': 'I am very interested in this position and would love to contribute to your team.'
        }
    )
    
    return Application.objects.filter(applicant=demo_applicant).select_related('listing', 'listing__recruiter').order_by('-created_at')