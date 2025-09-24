from django.shortcuts import render, get_object_or_404, redirect
from .models import JobPosting, Application
from accounts.models import Applicant
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    search_term = request.GET.get('search')
    if search_term:
        job_postings = JobPosting.objects.filter(title__icontains=search_term)
    else:
        job_postings = JobPosting.objects.all()
    template_data = {}
    template_data['title'] = 'HireMap - Jobs'
    template_data['job_postings'] = job_postings
    return render(request, 'jobs/index.html', {'template_data': template_data})

@login_required
def detail(request, job_id):
    job = get_object_or_404(JobPosting, id=job_id)

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("accounts:accounts.login")
        # Get the logged-in user's applicant profile
        print("post request received")
        message = request.POST.get("message", "")
        applicant = get_object_or_404(Applicant, user=request.user)
        Application.objects.create(
            applicant=applicant,
            listing=job,
            message=message,
        )

        return redirect("jobs:detail", job_id=job.id)
    template_data = {
        "title": f"HireMap - {job.title}",
        "job": job,   
    }
    return render(request, "jobs/job_detail.html", {
        "title": f"HireMap - {job.title}",
        "job": job
    })