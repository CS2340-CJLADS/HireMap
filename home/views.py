from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.decorators import applicant_required, recruiter_required
from accounts.models import Applicant, Project
from jobs.models import JobPosting, Application
from django.db.models import Q, Value, CharField
from django.db.models.functions import Concat

# Create your views here.
def index(request):
    template_data = {}
    template_data['title'] = 'HireMap - Home'
    return render(request, 'home/index.html', {'template_data': template_data})

def dashboard_router(request):
    user = request.user
    if hasattr(user, 'recruiter'):
        return redirect('home:recruiter')
    if hasattr(user, 'applicant'):
        return redirect('home:applicant')
    return redirect('home:index')

def applicant_dashboard(request):
    template_data = {'title': 'Applicant Dashboard'}
    return render(request, 'home/applicant_dashboard.html', {'template_data': template_data})

def recruiter_dashboard(request):
    template_data = {'title': 'Recruiter Dashboard'}
    return render(request, 'home/recruiter_dashboard.html', {'template_data': template_data})

def job_search_dashboard(request):
    """New job search dashboard with split-screen layout - No login required for testing"""
    
    # Get filter parameters (reuse existing jobs logic)
    search_term = request.GET.get('search')
    location = request.GET.get('location')
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
    
    template_data = {
        'title': 'Job Search Dashboard',
        'job_postings': job_postings,
        'search_term': search_term,
        'applied_job_ids': applied_job_ids,
        'recent_applications': recent_applications,
        'total_applications': total_applications,
        'total_projects': total_projects,
        'user_is_applicant': request.user.is_authenticated and hasattr(request.user, 'applicant'),
    }
    
    return render(request, 'home/job_search_dashboard.html', {'template_data': template_data})

@login_required
@applicant_required
def profile_view(request):
    """View and edit applicant profile"""
    applicant = request.user.applicant
    
    template_data = {
        'title': 'My Profile',
        'applicant': applicant
    }
    return render(request, 'accounts/profile_edit.html', {'template_data': template_data})

@login_required
@recruiter_required
def recruiter_profile_view(request):
    """View and edit recruiter profile"""
    recruiter = request.user.recruiter
    
    template_data = {
        'title': 'My Profile',
        'recruiter': recruiter
    }
    return render(request, 'home/recruiter_profile.html', {'template_data': template_data})

@login_required
@recruiter_required
def recruiter_profile_edit(request):
    """Edit recruiter profile"""
    recruiter = request.user.recruiter
    
    if request.method == 'POST':
        recruiter.first_name = request.POST.get('first_name', '').strip()
        recruiter.last_name = request.POST.get('last_name', '').strip()
        recruiter.company_name = request.POST.get('company_name', '').strip()
        recruiter.location = request.POST.get('location', '').strip()
        recruiter.save()
        return redirect('home:recruiter_profile')
    
    template_data = {
        'title': 'Edit Profile',
        'recruiter': recruiter
    }
    return render(request, 'home/recruiter_profile_edit.html', {'template_data': template_data})

@login_required
@recruiter_required
def search_candidates(request):
    """Search and filter job seekers"""
    # Get all applicants
    applicants = Applicant.objects.all()
    
    # Apply filters
    search_term = request.GET.get('search', '')
    skills_filter = request.GET.get('skills', '')
    location_filter = request.GET.get('location-value', '') or request.GET.get('location', '')
    availability_filter = request.GET.get('availability', '')
    education_filter = request.GET.get('education', '')
    
    # Build query
    query = Q()
    
    if search_term:
        # Create a computed full name field for searching  
        applicants = applicants.annotate(
            full_name=Concat('first_name', Value(' '), 'last_name', output_field=CharField())
        )
        
        query &= (
            Q(first_name__icontains=search_term) |
            Q(last_name__icontains=search_term) |
            Q(full_name__icontains=search_term) |  # Add full name search
            Q(skills__icontains=search_term) |
            Q(education__icontains=search_term) |
            Q(experience__icontains=search_term) | 
            Q(project_set__title__icontains=search_term) |  # Search project titles
            Q(project_set__description__icontains=search_term) |  # Search project descriptions
            Q(project_set__technologies__icontains=search_term)  # Search project technologies
        )

        applicants = applicants.distinct()  # Ensure distinct applicants after joins
    
    if skills_filter:
        skills_list = [skill.strip() for skill in skills_filter.split(',')]
        for skill in skills_list:
            query &= Q(skills__icontains=skill)
    
    if location_filter:
        query &= Q(location__icontains=location_filter)
    
    if availability_filter:
        query &= Q(availability=availability_filter)
    
    if education_filter:
        query &= Q(education__icontains=education_filter)
    
    # Apply filters
    applicants = applicants.filter(query)
    
    # Get projects for each applicant
    applicants_with_projects = []
    for applicant in applicants:
        projects = Project.objects.filter(applicant=applicant)
        temp = {
            'applicant': applicant,
            'projects': projects
            }
        if applicant.get_privacy_settings().show_skills:
            temp['skills'] = applicant.skills
        if applicant.get_privacy_settings().show_education:
            temp['education'] = applicant.education
        if applicant.get_privacy_settings().show_experience:
            temp['experience'] = applicant.experience
        if applicant.get_privacy_settings().show_links:
            temp['links'] = applicant.links
        if applicant.get_privacy_settings().show_phone:
            temp['phone'] = applicant.phone
        if applicant.get_privacy_settings().show_location:
            temp['location'] = applicant.location
        if applicant.get_privacy_settings().show_availability:
            temp['availability'] = applicant.availability
        applicants_with_projects.append(temp)
    
    template_data = {
        'title': 'Search Candidates',
        'applicants_with_projects': applicants_with_projects,
        'total_candidates': len(applicants_with_projects),
        'filters': {
            'search': search_term,
            'skills': skills_filter,
            'location': location_filter,
            'availability': availability_filter,
            'education': education_filter,
        }
    }
    
    return render(request, 'home/search_candidates.html', {'template_data': template_data})

def my_applications(request):
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
    return render(request, 'home/my_applications.html', {'template_data': template_data})

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