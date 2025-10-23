from django.db import models
from django.contrib.auth.models import User
from accounts.models import Applicant

# Create your models here.

class SavedSearch(models.Model):
    """Model for saving recruiter search criteria"""
    recruiter = models.ForeignKey('accounts.Recruiter', on_delete=models.CASCADE, related_name='saved_searches')
    name = models.CharField(max_length=100, help_text="Name for this search")
    description = models.TextField(blank=True, help_text="Optional description")
    
    # Search criteria
    skills_search = models.CharField(max_length=500, blank=True, help_text="Skills to search for")
    location_search = models.CharField(max_length=200, blank=True, help_text="Location preference")
    experience_level = models.CharField(max_length=50, blank=True, help_text="Experience level (entry, mid, senior)")
    education_level = models.CharField(max_length=50, blank=True, help_text="Education level")
    availability = models.CharField(max_length=50, blank=True, help_text="Availability status")
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    remote_preference = models.BooleanField(default=False, help_text="Remote work preference")
    visa_sponsorship = models.BooleanField(default=False, help_text="Visa sponsorship required")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, help_text="Whether to send notifications for this search")
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.recruiter.company_name}"


class SavedCandidate(models.Model):
    """Model for saving/favoriting candidates"""
    recruiter = models.ForeignKey('accounts.Recruiter', on_delete=models.CASCADE, related_name='saved_candidates')
    candidate = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name='saved_by_recruiters')
    notes = models.TextField(blank=True, help_text="Recruiter's notes about this candidate")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['recruiter', 'candidate']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.candidate.user.username} saved by {self.recruiter.company_name}"


class CandidateNotification(models.Model):
    """Model for tracking notifications about candidates"""
    NOTIFICATION_TYPES = [
        ('new_match', 'New Candidate Match'),
        ('candidate_applied', 'Saved Candidate Applied'),
        ('profile_updated', 'Saved Candidate Updated Profile'),
        ('job_match', 'Candidate Matches Job Posting'),
    ]
    
    recruiter = models.ForeignKey('accounts.Recruiter', on_delete=models.CASCADE, related_name='notifications')
    candidate = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    
    # Related objects (optional)
    saved_search = models.ForeignKey(SavedSearch, on_delete=models.CASCADE, null=True, blank=True)
    job_posting = models.ForeignKey('jobs.JobPosting', on_delete=models.CASCADE, null=True, blank=True)
    
    # Status
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.recruiter.company_name}"
