from django.db import models

# Create your models here.
class Applicant(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, 
                                primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    skills = models.TextField(blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    links = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.__str__() + f", {self.first_name} {self.last_name}"
    
class Recruiter(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, 
                                primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    company_name = models.CharField(max_length=100)

    def __str__(self):
        return self.user.__str__() + ", " + str(self.company_name)

