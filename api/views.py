from django.http import JsonResponse, Http404
from jobs.models import JobPosting
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from jobs.models import Application
import json
from django.db.models import Prefetch

def _serialize_jobposting(j: JobPosting) -> dict:
    """
    Minimal, non-invasive serializer that matches your existing schema.
    - Uses recruiter.company_name for "company".
    - Keeps your original field names (skills_required, salary_min/max, remote, etc).
    - Adds a few convenience aliases ("skills", "salary") that the front end can use,
      without changing your database or admin.
    """
    company = getattr(j.recruiter, "company_name", "")
    return {
        "id": j.id,
        "title": j.title,
        "company": company,                  # derived from recruiter
        "location": j.location,              # address string used by the map
        "description": j.description,
        "skills_required": j.skills_required,
        "skills": j.skills_required,         # convenience alias for UI
        "salary_min": str(j.salary_min),
        "salary_max": str(j.salary_max),
        "salary": f"{j.salary_min} - {j.salary_max}",  # convenience string
        "remote": j.remote,
        "visa_sponsorship": j.visa_sponsorship,
        # No "work_type" here (not in your model). UI already tolerates missing.
    }


def jobs_list(request):
    qs = JobPosting.objects.select_related("recruiter").order_by("-id")
    data = [_serialize_jobposting(j) for j in qs]
    return JsonResponse(data, safe=False)


def job_detail(request, pk: int):
    try:
        j = JobPosting.objects.select_related("recruiter").get(pk=pk)
    except JobPosting.DoesNotExist:
        raise Http404
    return JsonResponse(_serialize_jobposting(j))


@csrf_exempt
@require_http_methods(["PATCH"])
@login_required
def update_application_status(request, pk: int):
    """
    Recruiter moves an application to a new stage.
    PATCH body: {"status": "interview"}
    """
    try:
        app = Application.objects.select_related("listing__recruiter").get(pk=pk)
    except Application.DoesNotExist:
        return JsonResponse({"error": "not found"}, status=404)

    recruiter = app.listing.recruiter.user  # adjust if Recruiter has `user` field
    if request.user != recruiter and not request.user.is_staff:
        return JsonResponse({"error": "forbidden"}, status=403)

    data = json.loads(request.body.decode())
    new_status = data.get("status")
    valid = [s[0] for s in Application.STATUS_CHOICES]
    if new_status not in valid:
        return JsonResponse({"error": f"invalid status, must be one of {valid}"}, status=400)

    app.status = new_status
    app.save(update_fields=["status", "updated_at"])
    return JsonResponse({"id": app.id, "status": app.status})


@login_required
def recruiter_board(request):
    """Return all applications grouped by status for this recruiter (optionally filtered by job ID)."""
    user = request.user
    job_id = request.GET.get("job")

    # Base queryset: all applications for this recruiter
    apps = Application.objects.filter(listing__recruiter__user=user).select_related("applicant", "listing")

    # Optional per-job filter for Kanban view
    if job_id:
        apps = apps.filter(listing_id=job_id)

    grouped = {}
    for a in apps:
        grouped.setdefault(a.status, []).append({
            "id": a.id,
            "applicant": str(a.applicant),
            "listing_title": a.listing.title,
            "status": a.status,
        })

    return JsonResponse(grouped)
