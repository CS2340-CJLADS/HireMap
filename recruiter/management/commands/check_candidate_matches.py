from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone
from accounts.models import Applicant
from jobs.models import JobPosting, Application
from recruiter.models import SavedSearch, SavedCandidate, CandidateNotification
from jobs.recommendations import get_recommended_applicants


class Command(BaseCommand):
    help = 'Check for new candidate matches and create notifications'

    def handle(self, *args, **options):
        self.stdout.write('Checking for candidate matches...')
        
        # Get all active saved searches
        saved_searches = SavedSearch.objects.filter(is_active=True)
        
        for saved_search in saved_searches:
            self.check_search_matches(saved_search)
        
        # Check for saved candidates who applied to new jobs
        self.check_saved_candidate_applications()
        
        self.stdout.write(
            self.style.SUCCESS('Successfully checked for candidate matches')
        )

    def check_search_matches(self, saved_search):
        """Check if there are new candidates matching a saved search"""
        recruiter = saved_search.recruiter
        
        # Build search criteria
        search_criteria = Q()
        
        if saved_search.skills_search:
            search_criteria &= Q(skills__icontains=saved_search.skills_search)
        
        if saved_search.location_search:
            search_criteria &= Q(location__icontains=saved_search.location_search)
        
        if saved_search.experience_level:
            search_criteria &= Q(experience__icontains=saved_search.experience_level)
        
        if saved_search.education_level:
            search_criteria &= Q(education__icontains=saved_search.education_level)
        
        if saved_search.availability:
            search_criteria &= Q(availability=saved_search.availability)
        
        # Find matching candidates
        matching_candidates = Applicant.objects.filter(search_criteria)
        
        # Check if we already have notifications for these candidates
        existing_notifications = CandidateNotification.objects.filter(
            recruiter=recruiter,
            saved_search=saved_search,
            notification_type='new_match'
        ).values_list('candidate_id', flat=True)
        
        # Create notifications for new matches
        new_matches = matching_candidates.exclude(user_id__in=existing_notifications)
        
        for candidate in new_matches[:5]:  # Limit to 5 new matches per search
            CandidateNotification.objects.create(
                recruiter=recruiter,
                candidate=candidate,
                notification_type='new_match',
                title=f'New candidate match for "{saved_search.name}"',
                message=f'{candidate.first_name} {candidate.last_name} matches your saved search criteria.',
                saved_search=saved_search
            )
        
        if new_matches.exists():
            self.stdout.write(f'Created notifications for {new_matches.count()} new matches for search "{saved_search.name}"')

    def check_saved_candidate_applications(self):
        """Check if saved candidates applied to new jobs"""
        from jobs.models import Application
        
        # Get all saved candidates
        saved_candidates = SavedCandidate.objects.all()
        
        for saved_candidate in saved_candidates:
            recruiter = saved_candidate.recruiter
            candidate = saved_candidate.candidate
            
            # Check if candidate applied to any jobs recently (last 24 hours)
            recent_applications = Application.objects.filter(
                applicant=candidate,
                created_at__gte=timezone.now() - timezone.timedelta(days=1)
            )
            
            for application in recent_applications:
                # Check if we already notified about this application
                existing = CandidateNotification.objects.filter(
                    recruiter=recruiter,
                    candidate=candidate,
                    job_posting=application.listing,
                    notification_type='candidate_applied'
                ).exists()
                
                if not existing:
                    CandidateNotification.objects.create(
                        recruiter=recruiter,
                        candidate=candidate,
                        notification_type='candidate_applied',
                        title=f'Saved candidate applied to new job',
                        message=f'{candidate.first_name} {candidate.last_name} applied to "{application.listing.title}" at {application.listing.recruiter.company_name}.',
                        job_posting=application.listing
                    )
