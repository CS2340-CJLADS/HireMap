from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import RecruiterForm, ApplicantForm, CustomUserCreationForm
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.password_validation import password_validators_help_texts
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Location, Applicant, Recruiter, ApplicantPrivacySettings, Project
from .decorators import applicant_required, recruiter_required

# Create your views here.
def index(request):
    template_data = {}
    template_data['title'] = 'HireMap - Accounts'
    return render(request, 'accounts/index.html', {'template_data': template_data})
        
def signup(request):
    template_data = {}
    template_data['title'] = 'HireMap - Signup'
    if request.method == 'GET':
        return render(request, 'accounts/signup.html', {'template_data' : template_data})    

    if request.method == 'POST':
        # Debug print to see what data we're getting
        
        user_form = CustomUserCreationForm(request.POST, prefix='user')
        applicant_form = ApplicantForm(request.POST, prefix='applicant')
        recruiter_form = RecruiterForm(request.POST, prefix='recruiter')
        
        # Get user type to determine which path to take
        user_type = request.POST.get('user_type')
        
        # Check if user form is valid first
        if user_form.is_valid():
            # Check user type and validate appropriate form
            if user_type == 'recruiter' and recruiter_form.is_valid():
                user = user_form.save()
                recruiter = recruiter_form.save(commit=False)
                recruiter.user = user
                recruiter.save()
                return redirect('accounts:login')
                
            elif user_type == 'applicant' and applicant_form.is_valid():
                user = user_form.save()
                applicant = applicant_form.save(commit=False)
                applicant.user = user
                applicant.availability = request.POST.get('applicant-availability', 'open-to-work')
                applicant.save()
                return redirect('accounts:login')
                
            else:
                # Form validation failed for the specific user type
                template_data['error'] = 'Please fill in all required fields correctly.'
                return render(request, 'accounts/signup.html', {'template_data': template_data})
        else:
            template_data['error'] = 'Please review the highlighted fields.'
            template_data['user_form_errors'] = user_form.errors
            template_data['password_help_texts'] = password_validators_help_texts()
            return render(request, 'accounts/signup.html', {'template_data': template_data})

def login(request):
    template_data = {}
    template_data['title'] = 'HireMap - Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html', {'template_data' : template_data})
    elif request.method == 'POST':
        # The login form uses an "email" input; authenticate with Django's username field
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is None:
            template_data['error'] = 'The email or password is incorrect.'
            return render(request, 'accounts/login.html', {'template_data' : template_data})
        else: 
            auth_login(request, user)
            # Determine user type by checking which profile exists
            if hasattr(user, 'recruiter'):
                return redirect('recruiter:dashboard')  # Redirect to recruiter dashboard
            elif hasattr(user, 'applicant'):
                return redirect('seeker:dashboard')  # Redirect to seeker dashboard
            else:
                # Fallback if no profile exists
                return redirect('home:index')

@login_required
def logout(request):
    auth_logout(request)
    template_data = {'title': 'Signed Out'}
    return render(request, 'signout.html', {'template_data': template_data})

def get_locations(request):
    """API endpoint to get locations using real-time geocoding"""
    query = request.GET.get('q', '').strip()
    
    if not query or len(query) < 2:
        # Return remote options for empty/short queries
        remote_options = [
            {'id': 'remote-us', 'name': 'Remote - US', 'is_remote': True, 'country': 'United States', 'city': 'Remote', 'state_province': '', 'is_major_city': True},
            {'id': 'remote-global', 'name': 'Remote - Global', 'is_remote': True, 'country': 'Global', 'city': 'Remote', 'state_province': '', 'is_major_city': True},
            {'id': 'remote-na', 'name': 'Remote - North America', 'is_remote': True, 'country': 'North America', 'city': 'Remote', 'state_province': '', 'is_major_city': True},
            {'id': 'remote-europe', 'name': 'Remote - Europe', 'is_remote': True, 'country': 'Europe', 'city': 'Remote', 'state_province': '', 'is_major_city': True},
            {'id': 'remote-anywhere', 'name': 'Remote - Anywhere', 'is_remote': True, 'country': 'Global', 'city': 'Remote', 'state_province': '', 'is_major_city': True},
        ]
        return JsonResponse({
            'locations': remote_options,
            'total': len(remote_options),
            'query': query
        })
    
    try:
        # Use OpenStreetMap Nominatim API for real-time geocoding
        # This can handle ANY location in the world
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': query,
            'format': 'json',
            'addressdetails': 1,
            'limit': 10,
            'countrycodes': '',  # Search globally
            'featuretype': 'city,town,village,hamlet',  # Focus on populated places
        }
        
        headers = {
            'User-Agent': 'HireMap-Location-Search/1.0'  # Required by Nominatim
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=5)
        response.raise_for_status()
        
        results = response.json()
        
        location_list = []
        for result in results:
            address = result.get('address', {})
            display_name = result.get('display_name', '')
            
            # Extract location components
            city = (address.get('city') or 
                   address.get('town') or 
                   address.get('village') or 
                   address.get('hamlet') or 
                   address.get('suburb') or 
                   'Unknown')
            
            state = (address.get('state') or 
                    address.get('county') or 
                    address.get('region') or 
                    '')
            
            country = address.get('country', 'Unknown')
            
            # Create a clean display name
            if state and country:
                clean_name = f"{city}, {state}, {country}"
            elif country:
                clean_name = f"{city}, {country}"
            else:
                clean_name = city
            
            location_list.append({
                'id': f"geocoded-{result.get('place_id', 'unknown')}",
                'name': clean_name,
                'is_remote': False,
                'country': country,
                'city': city,
                'state_province': state,
                'is_major_city': False,
                'is_geocoded': True,
                'lat': result.get('lat'),
                'lon': result.get('lon'),
                'full_display': display_name
            })
        
        # Add the original query as a custom option
        location_list.append({
            'id': 'custom',
            'name': f'"{query}" (Use as entered)',
            'is_remote': False,
            'country': 'Custom',
            'city': query,
            'state_province': '',
            'is_major_city': False,
            'is_custom': True,
        })
        
        return JsonResponse({
            'locations': location_list,
            'total': len(location_list),
            'query': query
        })
        
    except requests.RequestException as e:
        # Fallback to custom location if API fails
        return JsonResponse({
            'locations': [{
                'id': 'custom',
                'name': f'"{query}" (Use as entered)',
                'is_remote': False,
                'country': 'Custom',
                'city': query,
                'state_province': '',
                'is_major_city': False,
                'is_custom': True,
            }],
            'total': 1,
            'query': query,
            'error': 'Geocoding service temporarily unavailable'
        })


@login_required
def profile_view(request, user_id=None):
    """View profile - either own profile or public profile of another user"""
    if user_id:
        # Viewing someone else's profile
        target_user = get_object_or_404(User, id=user_id)
        
        if hasattr(target_user, 'applicant'):
            # Viewing an applicant's profile
            applicant = target_user.applicant
            profile_data = applicant.get_public_profile_data()
            
            # Get projects if privacy allows
            privacy = applicant.get_privacy_settings()
            projects = []
            if privacy.show_projects:
                projects = Project.objects.filter(applicant=applicant)
            
            template_data = {
                'title': f"{applicant.first_name} {applicant.last_name} - Profile",
                'profile_data': profile_data,
                'projects': projects,
                'is_own_profile': False,
                'user_type': 'applicant',
                'target_user': target_user,
            }
            return render(request, 'accounts/public_applicant_profile.html', {'template_data': template_data})
            
        elif hasattr(target_user, 'recruiter'):
            # Viewing a recruiter's profile
            recruiter = target_user.recruiter
            template_data = {
                'title': f"{recruiter.first_name} {recruiter.last_name} - Profile",
                'recruiter': recruiter,
                'is_own_profile': False,
                'user_type': 'recruiter',
                'target_user': target_user,
            }
            return render(request, 'accounts/public_recruiter_profile.html', {'template_data': template_data})
    else:
        # Viewing own profile
        if hasattr(request.user, 'applicant'):
            return redirect('seeker:profile')
        elif hasattr(request.user, 'recruiter'):
            return redirect('accounts:recruiter_profile_edit')
        else:
            return redirect('home:index')


@login_required
@applicant_required
def profile_edit(request):
    """Edit applicant profile with privacy settings and project management"""
    applicant = request.user.applicant
    privacy_settings = applicant.get_privacy_settings()
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        # Handle project management actions
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
            return redirect('seeker:profile')
        
        elif action == 'edit':
            project_id = request.POST.get('project_id')
            if project_id:
                try:
                    project = Project.objects.get(id=project_id, applicant=applicant)
                    project.title = request.POST.get('title', '').strip()
                    project.description = request.POST.get('description', '').strip()
                    project.technologies = request.POST.get('technologies', '').strip()
                    project.url = request.POST.get('url', '').strip()
                    project.save()
                except Project.DoesNotExist:
                    pass
            return redirect('seeker:profile')
        
        elif action == 'delete':
            project_id = request.POST.get('project_id')
            if project_id:
                try:
                    project = Project.objects.get(id=project_id, applicant=applicant)
                    project.delete()
                except Project.DoesNotExist:
                    pass
            return redirect('seeker:profile')
        
        # Handle regular profile updates
        else:
            # Update basic profile information
            applicant.first_name = request.POST.get('first_name', '').strip()
            applicant.last_name = request.POST.get('last_name', '').strip()
            applicant.skills = request.POST.get('skills', '').strip()
            applicant.education = request.POST.get('education', '').strip()
            applicant.experience = request.POST.get('experience', '').strip()
            
            # Handle links as JSON array of {name, url} objects
            import json
            links_data = []
            link_names = request.POST.getlist('link_name[]')
            link_urls = request.POST.getlist('link_url[]')
            for name, url in zip(link_names, link_urls):
                name = name.strip()
                url = url.strip()
                if name and url:
                    links_data.append({'name': name, 'url': url})
            applicant.links = json.dumps(links_data) if links_data else ''
            applicant.phone = request.POST.get('phone', '').strip()
            applicant.location = request.POST.get('location-value', '').strip() or request.POST.get('location', '').strip()  # Keep for backward compatibility
            applicant.street_address = request.POST.get('street_address', '').strip()
            applicant.post_code = request.POST.get('post_code', '').strip()
            applicant.city = request.POST.get('city', '').strip()
            applicant.state = request.POST.get('state', '').strip()
            applicant.country = request.POST.get('country', 'USA').strip()
            applicant.availability = request.POST.get('availability', 'open-to-work')
            applicant.save()
            
            # Update privacy settings
            privacy_settings.show_skills = bool(request.POST.get('show_skills'))
            privacy_settings.show_education = bool(request.POST.get('show_education'))
            privacy_settings.show_experience = bool(request.POST.get('show_experience'))
            privacy_settings.show_projects = bool(request.POST.get('show_projects'))
            privacy_settings.show_links = bool(request.POST.get('show_links'))
            privacy_settings.show_phone = bool(request.POST.get('show_phone'))
            privacy_settings.show_location = bool(request.POST.get('show_location'))
            privacy_settings.show_availability = bool(request.POST.get('show_availability'))
            privacy_settings.allow_email_contact = bool(request.POST.get('allow_email_contact'))
            privacy_settings.save()
            
            return redirect('seeker:profile')
    
    # Get projects for display
    projects = Project.objects.filter(applicant=applicant)
    
    template_data = {
        'title': 'Edit Profile',
        'applicant': applicant,
        'privacy_settings': privacy_settings,
        'projects': projects,
    }
    return render(request, 'accounts/profile_edit.html', {'template_data': template_data})


@login_required
@recruiter_required
def recruiter_profile_edit(request):
    """Edit recruiter profile"""
    recruiter = request.user.recruiter
    
    if request.method == 'POST':
        recruiter.first_name = request.POST.get('first_name', '').strip()
        recruiter.last_name = request.POST.get('last_name', '').strip()
        recruiter.company_name = request.POST.get('company_name', '').strip()
        recruiter.location = request.POST.get('location', '').strip()  # Keep for backward compatibility
        recruiter.street_address = request.POST.get('street_address', '').strip()
        recruiter.post_code = request.POST.get('post_code', '').strip()
        recruiter.city = request.POST.get('city', '').strip()
        recruiter.state = request.POST.get('state', '').strip()
        recruiter.country = request.POST.get('country', 'USA').strip()
        recruiter.save()
        return redirect('recruiter:profile')
    
    template_data = {
        'title': 'Edit Profile',
        'recruiter': recruiter,
    }
    return render(request, 'accounts/recruiter_profile_edit.html', {'template_data': template_data})


@login_required
@applicant_required
def manage_projects(request):
    """Manage applicant projects"""
    applicant = request.user.applicant
    
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
        
        elif action == 'edit':
            project_id = request.POST.get('project_id')
            if project_id:
                try:
                    project = Project.objects.get(id=project_id, applicant=applicant)
                    project.title = request.POST.get('title', '').strip()
                    project.description = request.POST.get('description', '').strip()
                    project.technologies = request.POST.get('technologies', '').strip()
                    project.url = request.POST.get('url', '').strip()
                    project.save()
                except Project.DoesNotExist:
                    pass
        
        elif action == 'delete':
            project_id = request.POST.get('project_id')
            if project_id:
                try:
                    project = Project.objects.get(id=project_id, applicant=applicant)
                    project.delete()
                except Project.DoesNotExist:
                    pass
        
        return redirect('accounts:manage_projects')
    
    projects = Project.objects.filter(applicant=applicant)
    
    template_data = {
        'title': 'Manage Projects',
        'projects': projects,
    }
    return render(request, 'accounts/manage_projects.html', {'template_data': template_data})


