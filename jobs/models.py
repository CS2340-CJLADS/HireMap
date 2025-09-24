from django.db import models


# Create your models here.
class JobPosting(models.Model):
    id = models.AutoField(primary_key = True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    skills_required = models.TextField()
    location = models.CharField(max_length=100)  # address string (used by the map)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2)
    remote = models.BooleanField(default=False)
    visa_sponsorship = models.BooleanField(default=False)
    recruiter = models.ForeignKey('accounts.Recruiter', on_delete=models.CASCADE)
    is_draft = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return "id: " + str(self.id) + ", " + str(self.recruiter.company_name) + ", " + str(self.title)
    

class Application(models.Model):
    id = models.AutoField(primary_key = True)
    applicant = models.ForeignKey('accounts.Applicant', on_delete = models.CASCADE)
    # Basically all applicant information will be pulled from here
    listing = models.ForeignKey('jobs.JobPosting', on_delete = models.CASCADE)
    message = models.TextField(blank = True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['applicant', 'listing'], name='unique_application_per_listing')
        ]

    def __str__(self):
        return str(self.id) + " - applicant: " + self.applicant.__str__() + ", listing: " + self.listing.__str__()
