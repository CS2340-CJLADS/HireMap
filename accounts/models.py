from django.db import models
from django.db.models import Q
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
    location = models.CharField(max_length=100, blank=True, null=True)  # Keep for backward compatibility
    
    # Address fields
    street_address = models.CharField(max_length=200, blank=True, null=True, help_text="Street address")
    post_code = models.CharField(max_length=20, blank=True, null=True, help_text="ZIP/Postal code")
    city = models.CharField(max_length=100, blank=True, null=True, help_text="City")
    state = models.CharField(max_length=100, blank=True, null=True, help_text="State")
    country = models.CharField(max_length=100, default='USA', help_text="Country")
    
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
    
    def get_links_list(self):
        """Parse links from JSON string and return list of dicts with name and url"""
        import json
        if not self.links:
            return []
        try:
            return json.loads(self.links)
        except (json.JSONDecodeError, TypeError):
            # Fallback for old format or invalid JSON
            return []
    
    def get_privacy_settings(self):
        """Get or create privacy settings for this applicant"""
        privacy_settings, created = ApplicantPrivacySettings.objects.get_or_create(
            applicant=self,
            defaults={
                'show_skills': True,
                'show_education': True,
                'show_experience': True,
                'show_projects': True,
                'show_links': True,
                'show_phone': False,
                'show_location': True,
                'show_availability': True,
                'allow_email_contact': True,
            }
        )
        return privacy_settings
    
    def get_public_profile_data(self):
        """Get profile data filtered by privacy settings for public viewing"""
        privacy = self.get_privacy_settings()
        profile_data = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.user.email,
            'user_id': self.user.id,
        }
        
        if privacy.show_skills and self.skills:
            profile_data['skills'] = self.skills
        if privacy.show_education and self.education:
            profile_data['education'] = self.education
        if privacy.show_experience and self.experience:
            profile_data['experience'] = self.experience
        if privacy.show_links and self.links:
            profile_data['links'] = self.links
        if privacy.show_phone and self.phone:
            profile_data['phone'] = self.phone
        if privacy.show_location and self.location:
            profile_data['location'] = self.location
        if privacy.show_availability:
            profile_data['availability'] = self.availability
        if privacy.allow_email_contact:
            profile_data['allow_email_contact'] = True
            
        return profile_data
    
    def get_public_projects(self):
        """Get projects that are visible to the public based on privacy settings"""
        privacy = self.get_privacy_settings()
        if privacy.show_projects:
            return self.project_set.all()
        return Project.objects.none()
    


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
    location = models.CharField(max_length=100, blank=True, null=True)  # Keep for backward compatibility
    
    # Address fields
    street_address = models.CharField(max_length=200, blank=True, null=True, help_text="Street address")
    post_code = models.CharField(max_length=20, blank=True, null=True, help_text="ZIP/Postal code")
    city = models.CharField(max_length=100, blank=True, null=True, help_text="City")
    state = models.CharField(max_length=100, blank=True, null=True, help_text="State")
    country = models.CharField(max_length=100, default='USA', help_text="Country")

    def __str__(self):
        return self.user.__str__() + f", {self.first_name} {self.last_name}" + ", " + str(self.company_name)
    


class ApplicantPrivacySettings(models.Model):
    """Privacy settings for applicant profiles - controls what recruiters can see"""
    applicant = models.OneToOneField(Applicant, on_delete=models.CASCADE, related_name='privacy_settings')
    
    # Profile visibility toggles
    show_skills = models.BooleanField(default=True, help_text="Show skills to recruiters")
    show_education = models.BooleanField(default=True, help_text="Show education to recruiters")
    show_experience = models.BooleanField(default=True, help_text="Show experience to recruiters")
    show_projects = models.BooleanField(default=True, help_text="Show projects to recruiters")
    show_links = models.BooleanField(default=True, help_text="Show links to recruiters")
    show_phone = models.BooleanField(default=False, help_text="Show phone number to recruiters")
    show_location = models.BooleanField(default=True, help_text="Show location to recruiters")
    show_availability = models.BooleanField(default=True, help_text="Show availability status to recruiters")
    
    # Contact preferences
    allow_email_contact = models.BooleanField(default=True, help_text="Allow recruiters to email you")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Privacy settings for {self.applicant.first_name} {self.applicant.last_name}"


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