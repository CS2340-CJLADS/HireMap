from django.shortcuts import render

# Create your views here.
def index(request):
    template_data = {}
    template_data['title'] = 'HireMap - Jobs'
    return render(request, 'jobs/index.html', {'template_data': template_data})