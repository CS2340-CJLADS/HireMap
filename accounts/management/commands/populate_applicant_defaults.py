from django.core.management.base import BaseCommand
from accounts.models import Applicant

class Command(BaseCommand):
    help = 'Populate default values for existing applicants'

    def handle(self, *args, **options):
        # Get all applicants without availability set
        applicants = Applicant.objects.filter(availability__isnull=True)
        
        updated_count = 0
        for applicant in applicants:
            # Set default availability
            applicant.availability = 'open-to-work'
            applicant.save()
            updated_count += 1
            
        self.stdout.write(
            self.style.SUCCESS(f'Updated {updated_count} applicants with default availability')
        )
