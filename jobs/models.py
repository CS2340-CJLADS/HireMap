from django.db import models

<<<<<<< Updated upstream
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
=======
class Job(models.Model):
    WORK_TYPES = [
        ("remote", "Remote"),
        ("onsite", "On-site"),
        ("hybrid", "Hybrid"),
    ]

    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    work_type = models.CharField(max_length=10, choices=WORK_TYPES, blank=True)
    salary = models.CharField(max_length=100, blank=True)
    skills = models.CharField(max_length=255, blank=True)
    summary = models.TextField(blank=True)
    description = models.TextField(blank=True)
    responsibilities = models.TextField(blank=True)  # 1 bullet per line
    qualifications = models.TextField(blank=True)   # 1 bullet per line

    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.title} @ {self.company}"
>>>>>>> Stashed changes
