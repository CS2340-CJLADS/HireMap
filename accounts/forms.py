from django.contrib.auth.forms import UserCreationForm
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe
from django import forms
from django.forms import ModelForm
from .models import Recruiter, Applicant

class CustomErrorList(ErrorList):
    def __str__(self):
        if not self:
            return ''
        return mark_safe(''.join([f'<div class="alert alert-danger" role="alert">{e}</div>' for e in self]))
class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1',
        'password2']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs.update(
                {'class': 'form-control'}
            )
class RecruiterForm(ModelForm):
    class Meta:
        model = Recruiter
        fields = ['first_name', 'last_name', 'company_name']
        error_class = CustomErrorList
       

class ApplicantForm(ModelForm):
    class Meta:
        model = Applicant
        # Exclude 'links' since we handle it manually as JSON in the view
        fields = ['first_name', 'last_name', 'skills', 'education', 'experience', 'street_address', 'post_code', 'city', 'state', 'country']
        error_class = CustomErrorList
