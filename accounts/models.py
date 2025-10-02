from django.db import models
from django import forms

# Create your models here.
class Applicant(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, 
                                primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    skills = models.TextField(blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    projects = models.TextField(blank=True, null=True)  # Keep for backward compatibility
    links = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    
    # Availability status
    AVAILABILITY_CHOICES = [
        ('available', 'Available Now'),
        ('open-to-work', 'Open to Work'),
        ('not-looking', 'Not Looking'),
    ]
    availability = models.CharField(
        max_length=20, 
        choices=AVAILABILITY_CHOICES, 
        default='open-to-work',
        help_text="Current job search status"
    )

    def __str__(self):
        return self.user.__str__() + f", {self.first_name} {self.last_name}"


class Project(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name='project_set')
    title = models.CharField(max_length=200)
    description = models.TextField()
    technologies = models.CharField(max_length=500, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.applicant.first_name} {self.applicant.last_name} - {self.title}"


class Recruiter(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, 
                                primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    company_name = models.CharField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.__str__() + f", {self.first_name} {self.last_name}" + ", " + str(self.company_name)


class Location(models.Model):
    """Comprehensive location database for signup and job filtering"""
    name = models.CharField(max_length=200, unique=True)
    country = models.CharField(max_length=100)
    state_province = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100)
    is_remote = models.BooleanField(default=False)
    is_major_city = models.BooleanField(default=False)
    population = models.IntegerField(blank=True, null=True)
    timezone = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_major_city', '-population', 'name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['country', 'state_province']),
            models.Index(fields=['is_remote']),
            models.Index(fields=['is_major_city']),
        ]
    
    def __str__(self):
        if self.is_remote:
            return self.name
        elif self.state_province:
            return f"{self.city}, {self.state_province}"
        else:
            return f"{self.city}, {self.country}"
    
    @property
    def display_name(self):
        """Returns formatted display name for UI"""
        if self.is_remote:
            return self.name
        elif self.state_province:
            return f"{self.city}, {self.state_province}"
        else:
            return f"{self.city}, {self.country}"


# To figure out whether a user is an applicant or recruiter, take the request, take the user from the request, and use hasattr. For example:
# def someFunction(request):
#    user = request.user
#    if hasattr(user, 'applicant'):
#       do something here knowing we have an applicant