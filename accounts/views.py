from django.shortcuts import render, redirect
from .forms import RecruiterForm, ApplicantForm, CustomUserCreationForm
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.password_validation import password_validators_help_texts
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

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
        print("POST data:", dict(request.POST))
        
        user_form = CustomUserCreationForm(request.POST, prefix='user')
        applicant_form = ApplicantForm(request.POST, prefix='applicant')
        recruiter_form = RecruiterForm(request.POST, prefix='recruiter')
        
        # Get user type to determine which path to take
        user_type = request.POST.get('user_type')
        print(f"User type: {user_type}")
        
        # Check if user form is valid first
        if user_form.is_valid():
            print("User form is valid")
            
            # Check user type and validate appropriate form
            if user_type == 'recruiter' and recruiter_form.is_valid():
                print("Recruiter form is valid, creating user and recruiter")
                user = user_form.save()
                recruiter = recruiter_form.save(commit=False)
                recruiter.user = user
                recruiter.save()
                return redirect('accounts:accounts.login')
                
            elif user_type == 'applicant' and applicant_form.is_valid():
                print("Applicant form is valid, creating user and applicant")
                user = user_form.save()
                applicant = applicant_form.save(commit=False)
                applicant.user = user
                applicant.save()
                return redirect('accounts:accounts.login')
                
            else:
                # Form validation failed for the specific user type
                print("User form valid but specific form invalid")
                if user_type == 'recruiter':
                    print("Recruiter form errors:", recruiter_form.errors)
                elif user_type == 'applicant':
                    print("Applicant form errors:", applicant_form.errors)
                template_data['error'] = 'Please fill in all required fields correctly.'
                return render(request, 'accounts/signup.html', {'template_data': template_data})
        else:
            print("User form is invalid:", user_form.errors)
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
            user_type = request.POST.get('user_type')
            if (user_type == 'recruiter'):
                return redirect('recruiter.index')
            else:
                return redirect('applicant.index')

@login_required
def logout(request):
    auth_logout(request)
    template_data = {'title': 'Signed Out'}
    return render(request, 'signout.html', {'template_data': template_data})
