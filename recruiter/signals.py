from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import ApplicantPrivacySettings, Applicant
from recruiter.models import SavedSearch, CandidateNotification
from django.db.models import Q
from django.utils import timezone

@receiver(post_save, sender=ApplicantPrivacySettings)
def check_privacy_changes_for_matches(sender, instance, created, **kwargs):
    """Check for new matches when privacy settings are updated"""
    if not created:  # Only run on updates, not creation
        # Get all active saved searches
        saved_searches = SavedSearch.objects.filter(is_active=True)
        
        for saved_search in saved_searches:
            # Check if this applicant now matches the saved search
            if applicant_matches_saved_search(instance.applicant, saved_search):
                # Check if we already have a notification for this candidate and search
                existing_notification = CandidateNotification.objects.filter(
                    recruiter=saved_search.recruiter,
                    candidate=instance.applicant,
                    saved_search=saved_search,
                    notification_type='new_match'
                ).first()
                
                if not existing_notification:
                    # Create notification for new match
                    CandidateNotification.objects.create(
                        recruiter=saved_search.recruiter,
                        candidate=instance.applicant,
                        notification_type='new_match',
                        title=f'New candidate match for "{saved_search.name}"',
                        message=f'{instance.applicant.first_name} {instance.applicant.last_name} matches your saved search criteria.',
                        saved_search=saved_search
                    )

def applicant_matches_saved_search(applicant, saved_search):
    """Check if an applicant matches a saved search criteria with privacy filtering"""
    # Get applicant's privacy settings
    privacy = applicant.get_privacy_settings()
    
    # Check skills match
    if saved_search.skills_search:
        if not privacy.show_skills:
            return False
        if not applicant.skills or applicant.skills.strip() == '' or applicant.skills.lower() in ['none', 'no skills listed', 'no skills specified']:
            return False
        if saved_search.skills_search.lower() not in applicant.skills.lower():
            return False
    
    # Check location match
    if saved_search.location_search:
        if not privacy.show_location:
            return False
        if not applicant.location or applicant.location.strip() == '' or applicant.location.lower() in ['none', 'location not specified', 'no location specified']:
            return False
        if saved_search.location_search.lower() not in applicant.location.lower():
            return False
    
    # Check experience match
    if saved_search.experience_level:
        if not privacy.show_experience:
            return False
        if not applicant.experience or applicant.experience.strip() == '' or applicant.experience.lower() in ['none', 'no experience information provided', 'no experience specified']:
            return False
        if saved_search.experience_level.lower() not in applicant.experience.lower():
            return False
    
    # Check education match
    if saved_search.education_level:
        if not privacy.show_education:
            return False
        if not applicant.education or applicant.education.strip() == '' or applicant.education.lower() in ['none', 'no education information provided', 'no education specified']:
            return False
        if saved_search.education_level.lower() not in applicant.education.lower():
            return False
    
    # Check availability match
    if saved_search.availability:
        if not privacy.show_availability:
            return False
        if applicant.availability != saved_search.availability:
            return False
    
    return True

@receiver(post_save, sender=Applicant)
def check_new_applicant_for_matches(sender, instance, created, **kwargs):
    """Check for new matches when a new applicant is created"""
    if created:  # Only run on creation
        # Get all active saved searches
        saved_searches = SavedSearch.objects.filter(is_active=True)
        
        for saved_search in saved_searches:
            # Check if this new applicant matches the saved search
            if applicant_matches_saved_search(instance, saved_search):
                # Create notification for new match
                CandidateNotification.objects.create(
                    recruiter=saved_search.recruiter,
                    candidate=instance,
                    notification_type='new_match',
                    title=f'New candidate match for "{saved_search.name}"',
                    message=f'{instance.first_name} {instance.last_name} matches your saved search criteria.',
                    saved_search=saved_search
                )
