from django.shortcuts import render, redirect

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