from django.contrib.auth.forms import UserCreationForm

class RecruiterCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length = 30, required = True)
    last_name = forms.CharField(max_length=30, required=True)
    company_name = forms.CharField(max_length = 50, required = True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = str(self.max_length) + " characters or less"
            self.fields[fieldname].widget.attrs.update({'class': 'form-control'})
       

class ApplicantCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    skills = forms.TextField(widget=forms.Textarea, required=True)
    education = forms.TextField(widget=forms.Textarea, required=True)
    experience = forms.TextField(widget=forms.Textarea, required=True)
    links = forms.TextField(widget=forms.Textarea, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs.update({'class': 'form-control'})
