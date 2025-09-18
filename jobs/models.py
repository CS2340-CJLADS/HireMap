from django.db import models

# Create your models here.
class JobPosting(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    skills_required = models.TextField()
    location = models.CharField(max_length=100)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2)
    remote = models.BooleanField(default=False)
    visa_sponsorship = models.BooleanField(default=False)
    recruiter = models.ForeignKey('accounts.Recruiter', on_delete=models.CASCADE)

    def __str__(self):
        return self.title