from django.shortcuts import render, redirect
from .forms import RecruiterCreationForm, ApplicantCreationForm, CustomUserCreationForm
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
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
        user_form = CustomUserCreationForm(request.POST, prefix='user')
        applicant_form = ApplicantCreationForm(request.POST, prefix='applicant')
        recruiter_form = RecruiterCreationForm(request.POST, prefix='recruiter')

        if user_form.is_valid():
            if recruiter_form.is_valid():
                user = user_form.save()
                recruiter = recruiter_form.save(commit=False)
                recruiter.user = user
                recruiter.save()
                return redirect('accounts.login')
            elif applicant_form.is_valid():
                user = user_form.save()
                applicant = applicant_form.save(commit=False)
                applicant.user = user
                applicant.save()
                return redirect('accounts.login')
            else:
                return render(request, 'accounts/signup.html')
        else:
            return render(request, 'accounts/signup.html')

def login(request):
    template_data = {}
    template_data['title'] = 'HireMap - Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html', {'template_data' : template_data})
    elif request.method == 'POST':
        user = authenticate(request, username = request.POST['username'], password = request.POST['password'])
        if user is None:
            template_data['error'] = 'The email or password is incorrect.'
            return render(request, 'accounts/login.html', {'template_data' : template_data})
        else: 
            auth_login(request, user)
            return redirect('home.index')

@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')
