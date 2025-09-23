from django.shortcuts import render
from .models import JobPosting

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