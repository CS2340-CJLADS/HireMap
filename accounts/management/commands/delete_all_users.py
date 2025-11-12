from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Applicant, Recruiter, Project, ApplicantPrivacySettings
from jobs.models import JobPosting, Application
from recruiter.models import SavedSearch, SavedCandidate, CandidateNotification
from messages.models import Message


class Command(BaseCommand):
    help = 'Delete all users from the database (including applicants, recruiters, and all related data)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Skip confirmation prompt',
        )

    def handle(self, *args, **options):
        # Count users
        user_count = User.objects.count()
        applicant_count = Applicant.objects.count()
        recruiter_count = Recruiter.objects.count()
        project_count = Project.objects.count()
        job_count = JobPosting.objects.count()
        application_count = Application.objects.count()
        message_count = Message.objects.count()
        
        self.stdout.write(self.style.WARNING(f'\nThis will delete:'))
        self.stdout.write(f'  - {user_count} Users')
        self.stdout.write(f'  - {applicant_count} Applicants')
        self.stdout.write(f'  - {recruiter_count} Recruiters')
        self.stdout.write(f'  - {project_count} Projects')
        self.stdout.write(f'  - {job_count} Job Postings')
        self.stdout.write(f'  - {application_count} Applications')
        self.stdout.write(f'  - {message_count} Messages')
        self.stdout.write(f'  - All related data (SavedSearches, SavedCandidates, etc.)\n')
        
        if not options['force']:
            confirm = input('Are you sure you want to delete ALL users? Type "yes" to confirm: ')
            if confirm.lower() != 'yes':
                self.stdout.write(self.style.ERROR('Operation cancelled.'))
                return
        
        # Delete in order to respect foreign key constraints
        # Since most relationships use CASCADE, deleting Users will automatically delete related records
        # But we'll be explicit about the order
        
        self.stdout.write(self.style.WARNING('\nDeleting all users and related data...'))
        
        # Delete related records first (though CASCADE should handle this)
        # But being explicit helps avoid any issues
        
        # Delete messages
        Message.objects.all().delete()
        self.stdout.write('  [OK] Deleted all messages')
        
        # Delete applications
        Application.objects.all().delete()
        self.stdout.write('  [OK] Deleted all applications')
        
        # Delete job postings
        JobPosting.objects.all().delete()
        self.stdout.write('  [OK] Deleted all job postings')
        
        # Delete saved searches and candidates
        SavedSearch.objects.all().delete()
        SavedCandidate.objects.all().delete()
        CandidateNotification.objects.all().delete()
        self.stdout.write('  [OK] Deleted all saved searches and candidates')
        
        # Delete projects
        Project.objects.all().delete()
        self.stdout.write('  [OK] Deleted all projects')
        
        # Delete privacy settings
        ApplicantPrivacySettings.objects.all().delete()
        self.stdout.write('  [OK] Deleted all privacy settings')
        
        # Delete applicants and recruiters (these will cascade from User deletion, but being explicit)
        Applicant.objects.all().delete()
        Recruiter.objects.all().delete()
        self.stdout.write('  [OK] Deleted all applicants and recruiters')
        
        # Finally, delete all users
        deleted_count = User.objects.all().delete()[0]
        self.stdout.write(f'  [OK] Deleted {deleted_count} users')
        
        self.stdout.write(self.style.SUCCESS(f'\n[SUCCESS] Successfully deleted all users and related data!'))
        self.stdout.write(f'  Total users deleted: {deleted_count}')

