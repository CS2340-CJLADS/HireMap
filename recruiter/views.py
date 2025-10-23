from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from accounts.decorators import recruiter_required
from accounts.models import Applicant
from jobs.models import JobPosting, Application
from jobs.recommendations import get_recommended_applicants
from .models import SavedSearch, SavedCandidate, CandidateNotification

# Create your views here.

@login_required
@recruiter_required
def dashboard(request):
    """Recruiter dashboard"""
    recruiter = request.user.recruiter
    
    # Get filter parameters (same as seeker dashboard)
    search_term = request.GET.get('search')
    title = request.GET.get('title')
    location = request.GET.get('location')
    skills = request.GET.get('skills')
    salary_min = request.GET.get('salary_min')
    salary_max = request.GET.get('salary_max')
    visa_sponsorship = request.GET.get('visa_sponsorship')
    
    # Start with base queryset (all jobs, not just recruiter's)
    job_postings = JobPosting.objects.filter(is_draft=False, is_closed=False)
    
    # Apply search filter
    if search_term:
        job_postings = job_postings.filter(
            Q(title__icontains=search_term) |
            Q(recruiter__company_name__icontains=search_term) |
            Q(skills_required__icontains=search_term)
        )
    
    # Apply title filter
    if title:
        job_postings = job_postings.filter(title__icontains=title)
    
    # Apply skills filter
    if skills:
        job_postings = job_postings.filter(skills_required__icontains=skills)
    
    # Apply location filter
    if location:
        if location.lower() == 'remote':
            job_postings = job_postings.filter(remote=True)
        elif location.lower() == 'onsite' or location.lower() == 'on-site':
            job_postings = job_postings.filter(remote=False)
        else:
            # Search in location field for text matches
            job_postings = job_postings.filter(location__icontains=location)
    
    # Apply salary filters
    if salary_min:
        try:
            job_postings = job_postings.filter(salary_max__gte=float(salary_min))
        except ValueError:
            pass
    
    if salary_max:
        try:
            job_postings = job_postings.filter(salary_min__lte=float(salary_max))
        except ValueError:
            pass
    
    # Apply visa sponsorship filter
    if visa_sponsorship == 'true':
        job_postings = job_postings.filter(visa_sponsorship=True)
    
    # Get recruiter's jobs
    jobs = JobPosting.objects.filter(recruiter=recruiter).order_by('-created_at')
    
    # Get recent applications (exclude those with missing applicant IDs and self-applications)
    recent_applications = Application.objects.filter(
        listing__recruiter=recruiter,
        applicant__isnull=False
    ).exclude(
        applicant__user=recruiter.user  # Exclude applications where applicant is the same as recruiter
    ).select_related('applicant', 'listing').order_by('-created_at')[:10]
    
    
    # Add pagination for recruiter's own jobs
    page = request.GET.get('page', 1)
    paginator = Paginator(jobs, 12)  # Show 12 jobs per page
    jobs_page = paginator.get_page(page)
    
    # Get notifications for the recruiter
    all_notifications = CandidateNotification.objects.filter(recruiter=recruiter)
    notifications = all_notifications.order_by('-created_at')[:10]
    unread_count = all_notifications.filter(is_read=False).count()
    
    # Get saved searches for the recruiter
    saved_searches = SavedSearch.objects.filter(recruiter=recruiter, is_active=True).order_by('-created_at')[:10]
    
    template_data = {
        'title': 'Recruiter Dashboard',
        'recruiter': recruiter,
        'job_postings': job_postings,
        'jobs': jobs_page,
        'recent_applications': recent_applications,
        'total_jobs': jobs.count(),
        'total_applications': Application.objects.filter(listing__recruiter=recruiter).count(),
        'search_term': search_term,
        'paginator': paginator,
        'current_page': page,
        'notifications': notifications,
        'unread_count': unread_count,
        'saved_searches': saved_searches,
    }
    
    return render(request, 'recruiter/dashboard.html', {'template_data': template_data})

@login_required
@recruiter_required
def profile(request):
    """View and edit recruiter profile"""
    recruiter = request.user.recruiter
    
    template_data = {
        'title': 'My Profile',
        'recruiter': recruiter
    }
    return render(request, 'recruiter/profile.html', {'template_data': template_data})

@login_required
@recruiter_required
def job_new(request):
    """Create new job posting"""
    recruiter = request.user.recruiter
    
    if request.method == 'POST':
        # Get the action (publish or draft)
        action = request.POST.get('action', 'publish')
        is_draft = action == 'draft'
        
        # Create new job posting
        job = JobPosting.objects.create(
            title=request.POST.get('title', ''),
            description=request.POST.get('description', ''),
            skills_required=request.POST.get('skills_required', ''),
            location=request.POST.get('location', ''),
            salary_min=float(request.POST.get('salary_min', 0)),
            salary_max=float(request.POST.get('salary_max', 0)),
            remote=request.POST.get('remote') == 'on',
            visa_sponsorship=request.POST.get('visa_sponsorship') == 'on',
            recruiter=recruiter,
            is_draft=is_draft,
        )
        return redirect('recruiter:dashboard')
    
    template_data = {
        'title': 'Post New Job',
    }
    return render(request, 'recruiter/job_new.html', {'template_data': template_data})

@login_required
@recruiter_required
def job_edit(request, job_id):
    """Edit job posting"""
    recruiter = request.user.recruiter
    job = get_object_or_404(JobPosting, id=job_id, recruiter=recruiter)
    
    if request.method == 'POST':
        # Get the action (publish, draft, save, or unpublish)
        action = request.POST.get('action', 'save')
        
        # Update job fields
        job.title = request.POST.get('title', '')
        job.description = request.POST.get('description', '')
        job.skills_required = request.POST.get('skills_required', '')
        job.location = request.POST.get('location', '')
        job.salary_min = float(request.POST.get('salary_min', 0))
        job.salary_max = float(request.POST.get('salary_max', 0))
        job.remote = request.POST.get('remote') == 'on'
        job.visa_sponsorship = request.POST.get('visa_sponsorship') == 'on'
        
        # Handle different actions
        if action == 'publish':
            job.is_draft = False
        elif action == 'draft':
            job.is_draft = True
        elif action == 'unpublish':
            job.is_draft = True
        # For 'save' action, keep current draft status
        
        job.save()
        return redirect('recruiter:dashboard')
    
    template_data = {
        'title': 'Edit Job',
        'job': job,
    }
    return render(request, 'recruiter/job_edit.html', {'template_data': template_data})

@login_required
@recruiter_required
def job_applications(request, job_id):
    """View applications for a specific job"""
    recruiter = request.user.recruiter
    job = get_object_or_404(JobPosting, id=job_id, recruiter=recruiter)
    applications = Application.objects.filter(
        listing=job,
        applicant__isnull=False
    ).exclude(
        applicant__user=recruiter.user  # Exclude applications where applicant is the same as recruiter
    ).select_related('applicant').order_by('-created_at')
    
    # Check if JSON response is requested
    if request.GET.get('format') == 'json':
        from django.http import JsonResponse
        data = []
        for app in applications:
            data.append({
                'id': app.id,
                'name': f"{app.applicant.first_name} {app.applicant.last_name}",
                'email': app.applicant.user.username,
                'status': app.status,  # Use actual status from model
                'application_date': app.created_at.strftime('%Y-%m-%d'),
                'message': app.message,
                'applicant_id': app.applicant.pk,  # Use pk instead of id
            })
        return JsonResponse(data, safe=False)
    
    template_data = {
        'title': f'Applications for {job.title}',
        'job': job,
        'applications': applications,
    }
    return render(request, 'recruiter/job_applications.html', {'template_data': template_data})

@login_required
@recruiter_required
def job_delete(request, job_id):
    """Delete job posting"""
    recruiter = request.user.recruiter
    job = get_object_or_404(JobPosting, id=job_id, recruiter=recruiter)
    
    if request.method == 'POST':
        job.delete()
        return redirect('recruiter:dashboard')
    
    template_data = {
        'title': 'Delete Job',
        'job': job,
    }
    return render(request, 'recruiter/job_delete.html', {'template_data': template_data})

@login_required
@recruiter_required
def view_applicant(request, applicant_id):
    """View applicant profile"""
    recruiter = request.user.recruiter
    applicant = get_object_or_404(Applicant, pk=applicant_id)
    
    template_data = {
        'title': f'{applicant.first_name} {applicant.last_name}',
        'applicant': applicant,
    }
    return render(request, 'accounts/applicant_profile.html', {'template_data': template_data})

@login_required
@recruiter_required
def search_candidates(request):
    """Search candidates with recommendations"""
    recruiter = request.user.recruiter
    
    # Get filter parameters
    search_term = request.GET.get('search')
    skills_search = request.GET.get('skills') or request.GET.get('skills_search')
    location_search = request.GET.get('location') or request.GET.get('location_search')
    availability_search = request.GET.get('availability')
    education_search = request.GET.get('education')
    job_id = request.GET.get('job_id')
    candidate_id = request.GET.get('candidate_id')
    
    # Start with base queryset
    applicants = Applicant.objects.all().order_by('-user_id')
    
    # If candidate_id is provided, get the specific candidate for the right panel
    specific_candidate = None
    specific_candidate_projects = []
    if candidate_id:
        try:
            specific_candidate = Applicant.objects.get(user_id=candidate_id)
            # Get projects for the specific candidate
            from accounts.models import Project
            specific_candidate_projects = Project.objects.filter(applicant=specific_candidate)
            # Don't pre-populate search fields - let user search normally
        except Applicant.DoesNotExist:
            # If candidate doesn't exist, continue with normal search
            pass
    
    # Apply search filters
    if search_term:
        applicants = applicants.filter(
            Q(first_name__icontains=search_term) |
            Q(last_name__icontains=search_term) |
            Q(skills__icontains=search_term) |
            Q(education__icontains=search_term)
        )
    
    if skills_search:
        skills_list = [skill.strip() for skill in skills_search.split(',') if skill.strip()]
        for skill in skills_list:
            # Only include applicants who have skills visible and contain the search term
            # We need to filter out applicants whose skills are hidden by privacy settings
            from accounts.models import ApplicantPrivacySettings
            applicants = applicants.filter(
                skills__icontains=skill,
                privacy_settings__show_skills=True  # Only show applicants with visible skills
            ).exclude(
                Q(skills__isnull=True) | 
                Q(skills__exact='') | 
                Q(skills__exact='None') |
                Q(skills__icontains='No skills listed') |
                Q(skills__icontains='No skills specified')
            )
    
    if location_search:
        # Exclude applicants with no location or placeholder text
        applicants = applicants.filter(
            location__icontains=location_search,
            privacy_settings__show_location=True  # Only show applicants with visible location
        ).exclude(
            Q(location__isnull=True) | 
            Q(location__exact='') | 
            Q(location__exact='None') |
            Q(location__icontains='Location not specified') |
            Q(location__icontains='No location specified')
        )
    
    if availability_search:
        applicants = applicants.filter(availability=availability_search)
    
    if education_search:
        # Exclude applicants with no education or placeholder text
        applicants = applicants.filter(
            education__icontains=education_search,
            privacy_settings__show_education=True  # Only show applicants with visible education
        ).exclude(
            Q(education__isnull=True) | 
            Q(education__exact='') | 
            Q(education__exact='None') |
            Q(education__icontains='No education information provided') |
            Q(education__icontains='No education specified')
        )
    
    # Add pagination
    from django.core.paginator import Paginator
    page = request.GET.get('page', 1)
    paginator = Paginator(applicants, 12)  # Show 12 candidates per page
    applicants_page = paginator.get_page(page)
    
    # Get projects for each applicant on current page
    from accounts.models import Project
    applicants_with_projects = []
    for applicant in applicants_page:
        projects = Project.objects.filter(applicant=applicant)
        temp = {
            'applicant': applicant,
            'projects': projects
        }
        if applicant.get_privacy_settings().show_skills:
            temp['skills'] = applicant.skills
        if applicant.get_privacy_settings().show_education:
            temp['education'] = applicant.education
        if applicant.get_privacy_settings().show_experience:
            temp['experience'] = applicant.experience
        if applicant.get_privacy_settings().show_links:
            temp['links'] = applicant.links
        if applicant.get_privacy_settings().show_phone:
            temp['phone'] = applicant.phone
        if applicant.get_privacy_settings().show_location:
            temp['location'] = applicant.location
        if applicant.get_privacy_settings().show_availability:
            temp['availability'] = applicant.availability
        applicants_with_projects.append(temp)
    
    # Get recommended applicants if job is specified
    recommended_applicants = []
    if job_id:
        job = get_object_or_404(JobPosting, pk=job_id, recruiter=recruiter)
        recommended_applicants = get_recommended_applicants(job, limit=10)
    
    template_data = {
        'title': 'Search Candidates',
        'applicants_with_projects': applicants_with_projects,
        'total_candidates': paginator.count,
        'paginator': paginator,
        'current_page': page,
        'recommended_applicants': recommended_applicants,
        'search_term': search_term,
        'skills_search': skills_search,
        'location_search': location_search,
        'availability_search': availability_search,
        'education_search': education_search,
        'job_id': job_id,
        'candidate_id': candidate_id,
        'specific_candidate': specific_candidate,
        'specific_candidate_projects': specific_candidate_projects,
        'filters': {
            'search': search_term,
            'skills': skills_search,
            'location': location_search,
            'availability': availability_search,
            'education': education_search,
        }
    }
    
    return render(request, 'home/search_candidates.html', {'template_data': template_data})

@login_required
@recruiter_required
def get_applicant_info(request, applicant_id):
    """Get applicant info as JSON (for AJAX requests)"""
    from django.http import JsonResponse
    applicant = get_object_or_404(Applicant, pk=applicant_id)
    
    data = {}

    if applicant.get_privacy_settings().show_skills:
        data['skills'] = applicant.skills
    if applicant.get_privacy_settings().show_education:
        data['education'] = applicant.education
    if applicant.get_privacy_settings().show_experience:
        data['experience'] = applicant.experience
    if applicant.get_privacy_settings().show_location:
        data['location'] = applicant.location
    
    return JsonResponse(data)


# ============================================================================
# SAVED SEARCHES AND CANDIDATES
# ============================================================================

@login_required
@recruiter_required
def saved_searches(request):
    """View and manage saved searches"""
    recruiter = request.user.recruiter
    saved_searches = SavedSearch.objects.filter(recruiter=recruiter)
    
    template_data = {
        'title': 'Saved Searches',
        'saved_searches': saved_searches,
    }
    
    return render(request, 'recruiter/saved_searches.html', {'template_data': template_data})


@login_required
@recruiter_required
def save_search(request):
    """Save current search criteria"""
    if request.method == 'POST':
        try:
            recruiter = request.user.recruiter
            
            # Get search parameters from request
            name = request.POST.get('name', '')
            description = request.POST.get('description', '')
            skills_search = request.POST.get('skills', '')
            location_search = request.POST.get('location', '')
            experience_level = request.POST.get('experience_level', '')
            education_level = request.POST.get('education_level', '')
            availability = request.POST.get('availability', '')
            salary_min = request.POST.get('salary_min')
            salary_max = request.POST.get('salary_max')
            remote_preference = request.POST.get('remote_preference') == 'on'
            visa_sponsorship = request.POST.get('visa_sponsorship') == 'on'
            
            # Validate required fields
            if not name.strip():
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'message': 'Search name is required'}, status=400)
                else:
                    messages.error(request, 'Search name is required')
                    return redirect('recruiter:search_candidates')
            
            # Create saved search
            saved_search = SavedSearch.objects.create(
                recruiter=recruiter,
                name=name,
                description=description,
                skills_search=skills_search,
                location_search=location_search,
                experience_level=experience_level,
                education_level=education_level,
                availability=availability,
                salary_min=float(salary_min) if salary_min else None,
                salary_max=float(salary_max) if salary_max else None,
                remote_preference=remote_preference,
                visa_sponsorship=visa_sponsorship,
            )
            
            # Create notifications for matching candidates immediately
            create_notifications_for_saved_search(saved_search)
            
            # Check if this is an AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': f'Search "{name}" saved successfully!'})
            else:
                messages.success(request, f'Search "{name}" saved successfully!')
                return redirect('recruiter:saved_searches')
                
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': f'Error saving search: {str(e)}'}, status=500)
            else:
                messages.error(request, f'Error saving search: {str(e)}')
                return redirect('recruiter:search_candidates')
    
    return redirect('recruiter:search_candidates')


@login_required
@recruiter_required
def delete_saved_search(request, search_id):
    """Delete a saved search"""
    saved_search = get_object_or_404(SavedSearch, id=search_id, recruiter=request.user.recruiter)
    saved_search.delete()
    messages.success(request, 'Search deleted successfully!')
    return redirect('recruiter:saved_searches')


@login_required
@recruiter_required
def load_saved_search(request, search_id):
    """Load a saved search and redirect to search with parameters"""
    saved_search = get_object_or_404(SavedSearch, id=search_id, recruiter=request.user.recruiter)
    
    # Build URL parameters
    params = []
    if saved_search.skills_search:
        params.append(f'skills={saved_search.skills_search}')
    if saved_search.location_search:
        params.append(f'location={saved_search.location_search}')
    if saved_search.experience_level:
        params.append(f'experience_level={saved_search.experience_level}')
    if saved_search.education_level:
        params.append(f'education_level={saved_search.education_level}')
    if saved_search.availability:
        params.append(f'availability={saved_search.availability}')
    if saved_search.salary_min:
        params.append(f'salary_min={saved_search.salary_min}')
    if saved_search.salary_max:
        params.append(f'salary_max={saved_search.salary_max}')
    if saved_search.remote_preference:
        params.append('remote_preference=true')
    if saved_search.visa_sponsorship:
        params.append('visa_sponsorship=true')
    
    # Redirect to search with parameters
    url = '/recruiter/search-candidates/'
    if params:
        url += '?' + '&'.join(params)
    
    return redirect(url)


@login_required
@recruiter_required
def saved_candidates(request):
    """View saved candidates"""
    recruiter = request.user.recruiter
    saved_candidates = SavedCandidate.objects.filter(recruiter=recruiter)
    
    template_data = {
        'title': 'Saved Candidates',
        'saved_candidates': saved_candidates,
    }
    
    return render(request, 'recruiter/saved_candidates.html', {'template_data': template_data})


@login_required
@recruiter_required
@require_http_methods(["POST"])
def save_candidate(request, candidate_id):
    """Save/favorite a candidate"""
    recruiter = request.user.recruiter
    candidate = get_object_or_404(Applicant, pk=candidate_id)
    notes = request.POST.get('notes', '')
    
    # Create or update saved candidate
    saved_candidate, created = SavedCandidate.objects.get_or_create(
        recruiter=recruiter,
        candidate=candidate,
        defaults={'notes': notes}
    )
    
    if not created:
        saved_candidate.notes = notes
        saved_candidate.save()
    
    if request.headers.get('Content-Type') == 'application/json':
        return JsonResponse({'success': True, 'message': 'Candidate saved successfully!'})
    else:
        messages.success(request, 'Candidate saved successfully!')
        return redirect('recruiter:saved_candidates')


@login_required
@recruiter_required
@require_http_methods(["POST"])
def unsave_candidate(request, candidate_id):
    """Remove candidate from saved list"""
    recruiter = request.user.recruiter
    candidate = get_object_or_404(Applicant, pk=candidate_id)
    
    SavedCandidate.objects.filter(recruiter=recruiter, candidate=candidate).delete()
    
    if request.headers.get('Content-Type') == 'application/json':
        return JsonResponse({'success': True, 'message': 'Candidate removed from saved list!'})
    else:
        messages.success(request, 'Candidate removed from saved list!')
        return redirect('recruiter:saved_candidates')


@login_required
@recruiter_required
def notifications(request):
    """View notifications"""
    recruiter = request.user.recruiter
    notifications = CandidateNotification.objects.filter(recruiter=recruiter)
    
    template_data = {
        'title': 'Notifications',
        'notifications': notifications,
        'unread_count': notifications.filter(is_read=False).count(),
    }
    
    return render(request, 'recruiter/notifications.html', {'template_data': template_data})


@login_required
@recruiter_required
@require_http_methods(["POST"])
def mark_notification_read(request, notification_id):
    """Mark a notification as read"""
    notification = get_object_or_404(CandidateNotification, id=notification_id, recruiter=request.user.recruiter)
    notification.is_read = True
    notification.save()
    
    return JsonResponse({'success': True})


@login_required
@recruiter_required
@require_http_methods(["POST"])
def mark_all_notifications_read(request):
    """Mark all notifications as read"""
    CandidateNotification.objects.filter(recruiter=request.user.recruiter, is_read=False).update(is_read=True)
    
    return JsonResponse({'success': True})


def dismiss_notification(request, notification_id):
    """Dismiss (delete) a specific notification"""
    recruiter = request.user.recruiter
    try:
        notification = CandidateNotification.objects.get(id=notification_id, recruiter=recruiter)
        notification.delete()
        return JsonResponse({'success': True})
    except CandidateNotification.DoesNotExist:
        return JsonResponse({'error': 'Notification not found'}, status=404)


def create_notifications_for_saved_search(saved_search):
    """Create notifications for candidates matching a saved search"""
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