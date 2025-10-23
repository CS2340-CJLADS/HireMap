from django.core.management.base import BaseCommand
from django.db.models import Q
from recruiter.models import SavedSearch, CandidateNotification
from accounts.models import Applicant
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Check for new candidate matches for all saved searches'

    def add_arguments(self, parser):
        parser.add_argument(
            '--hours',
            type=int,
            default=24,
            help='Check for candidates added or privacy settings changed in the last N hours (default: 24)'
        )

    def handle(self, *args, **options):
        hours = options['hours']
        cutoff_time = timezone.now() - timedelta(hours=hours)
        
        # Get all active saved searches
        saved_searches = SavedSearch.objects.filter(is_active=True)
        
        total_notifications = 0
        
        for saved_search in saved_searches:
            notifications_created = self.check_search_matches(saved_search, cutoff_time)
            total_notifications += notifications_created
            
            if notifications_created > 0:
                self.stdout.write(
                    f'Created {notifications_created} notifications for search "{saved_search.name}"'
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Total notifications created: {total_notifications}')
        )

    def check_search_matches(self, saved_search, cutoff_time):
        """Check if there are new candidates matching a saved search"""
        recruiter = saved_search.recruiter
        
        # Build search criteria with privacy filtering (same as search_candidates view)
        search_criteria = Q()
        
        if saved_search.skills_search:
            # Only include applicants who have skills visible and contain the search term
            search_criteria &= Q(
                skills__icontains=saved_search.skills_search,
                privacy_settings__show_skills=True
            ) & ~(
                Q(skills__isnull=True) | 
                Q(skills__exact='') | 
                Q(skills__exact='None') |
                Q(skills__icontains='No skills listed') |
                Q(skills__icontains='No skills specified')
            )
        
        if saved_search.location_search:
            # Only include applicants who have location visible and contain the search term
            search_criteria &= Q(
                location__icontains=saved_search.location_search,
                privacy_settings__show_location=True
            ) & ~(
                Q(location__isnull=True) | 
                Q(location__exact='') | 
                Q(location__exact='None') |
                Q(location__icontains='Location not specified') |
                Q(location__icontains='No location specified')
            )
        
        if saved_search.experience_level:
            # Only include applicants who have experience visible and contain the search term
            search_criteria &= Q(
                experience__icontains=saved_search.experience_level,
                privacy_settings__show_experience=True
            ) & ~(
                Q(experience__isnull=True) | 
                Q(experience__exact='') | 
                Q(experience__exact='None') |
                Q(experience__icontains='No experience information provided') |
                Q(experience__icontains='No experience specified')
            )
        
        if saved_search.education_level:
            # Only include applicants who have education visible and contain the search term
            search_criteria &= Q(
                education__icontains=saved_search.education_level,
                privacy_settings__show_education=True
            ) & ~(
                Q(education__isnull=True) | 
                Q(education__exact='') | 
                Q(education__exact='None') |
                Q(education__icontains='No education information provided') |
                Q(education__icontains='No education specified')
            )
        
        if saved_search.availability:
            # Only include applicants who have availability visible
            search_criteria &= Q(
                availability=saved_search.availability,
                privacy_settings__show_availability=True
            )
        
        # Find matching candidates with privacy filtering
        matching_candidates = Applicant.objects.filter(search_criteria)
        
        # Filter for candidates who were added or had privacy settings changed recently
        recent_candidates = matching_candidates.filter(
            Q(user__date_joined__gte=cutoff_time) |  # New users
            Q(privacy_settings__updated_at__gte=cutoff_time)  # Privacy settings changed
        )
        
        # Check if we already have notifications for these candidates
        existing_notifications = CandidateNotification.objects.filter(
            recruiter=recruiter,
            saved_search=saved_search,
            notification_type='new_match'
        ).values_list('candidate_id', flat=True)
        
        # Create notifications for new matches
        new_matches = recent_candidates.exclude(user_id__in=existing_notifications)
        
        notifications_created = 0
        for candidate in new_matches[:5]:  # Limit to 5 new matches per search
            CandidateNotification.objects.create(
                recruiter=recruiter,
                candidate=candidate,
                notification_type='new_match',
                title=f'New candidate match for "{saved_search.name}"',
                message=f'{candidate.first_name} {candidate.last_name} matches your saved search criteria.',
                saved_search=saved_search
            )
            notifications_created += 1
        
        return notifications_created
