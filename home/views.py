from django.shortcuts import render

# Create your views here.
def index(request):
    template_data = {}
    template_data['title'] = 'HireMap - Home'
    return render(request, '../templates/index.html', {'template_data': template_data})