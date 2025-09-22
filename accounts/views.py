from django.shortcuts import render
from .forms import RecruiterCreationForm, ApplicantCreationForm
from .models import Recruiter, Applicant

# Create your views here.
def index(request):
    template_data = {}
    template_data['title'] = 'HireMap - Accounts'
    return render(request, 'accounts/index.html', {'template_data': template_data})


#Note that the page it's trying to redirect to is called accounts/RecruiterSignup, let David know if this should be updated.
#Otherwise it's mostly the same as the movies store with some extended help from GPT.
def RecruiterSignup(request):
    template_data = {}
    template_data['title'] = 'Signup (Recruiter)'
    if request.method == 'GET':
        template_data['form'] = RecruiterCreationForm()
        return render(request, 'accounts/RecruiterSignup.html', {'template_data' : template_data})
    elif request.method == 'POST':
        form = RecruiterCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Recruiter.objects.create(user = user, 
                                    first_name = form.cleaned_data['first_name'],
                                    last_name = form.cleaned_data['last_name'],
                                    company_name = form.cleaned_data['company_name']
            )
            messages.success(request, "Recruiter account created successfully.")         
            return redirect('accounts.RecruiterLogin')
        else:
            template_data['form'] = form
            return render(request, 'accounts/RecruiterSignup.html', {'template_data' : template_data})

def ApplicantSignup(request):
    template_data = {}
    template_data['title'] = 'Signup (Applicant)'

    if request.method == 'GET':
        template_data['form'] = ApplicantCreationForm()
        return render(request, 'accounts/ApplicantSignup.html', {'template_data': template_data})

    elif request.method == 'POST':
        form = ApplicantCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Applicant.objects.create(
                user=user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                skills=form.cleaned_data.get('skills', ''),
                education=form.cleaned_data.get('education', ''),
                experience=form.cleaned_data.get('experience', ''),
                links=form.cleaned_data.get('links', '')
            )
            messages.success(request, "Applicant account created successfully.")
            return redirect('accounts.login')
        else:
            template_data['form'] = form
            return render(request, 'accounts/applicant_signup.html', {'template_data': template_data})

def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html', {'template_data' : template_data})
    elif request.method == 'POST':
        user = authenticate(request, username = request.POST['username'], password = request.POST['password'])
        if user is None:
            template_data['error'] = 'The username or password is incorrect.'
            return render(request, 'accounts/login.html', {'template_data' : template_data})
        else: 
            auth_login(request, user)
            return redirect('home.index')

@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')
