from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.decorators import applicant_required, recruiter_required
from accounts.models import Applicant, Project
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

@login_required
@applicant_required
def profile_view(request):
    """View and edit applicant profile"""
    applicant = request.user.applicant
    
    template_data = {
        'title': 'My Profile',
        'applicant': applicant
    }
    return render(request, 'home/profile_edit.html', {'template_data': template_data})

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
        applicants_with_projects.append({
            'applicant': applicant,
            'projects': projects
        })
    
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