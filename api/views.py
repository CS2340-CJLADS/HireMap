from django.http import JsonResponse, Http404
from jobs.models import JobPosting


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
