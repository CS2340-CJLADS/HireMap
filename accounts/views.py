from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import RecruiterForm, ApplicantForm, CustomUserCreationForm
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.password_validation import password_validators_help_texts
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Location
import requests
import json

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
                return redirect('accounts:accounts.login')
                
            elif user_type == 'applicant' and applicant_form.is_valid():
                user = user_form.save()
                applicant = applicant_form.save(commit=False)
                applicant.user = user
                applicant.availability = request.POST.get('applicant-availability', 'open-to-work')
                applicant.save()
                return redirect('accounts:accounts.login')
                
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
                return redirect('home:recruiter')  # currently a placeholder
            elif hasattr(user, 'applicant'):
                return redirect('home:applicant')  # currently a placeholder
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
