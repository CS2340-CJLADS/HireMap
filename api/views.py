from django.http import JsonResponse, Http404
from jobs.models import Job

def _job_to_dict(job: Job) -> dict:
    return {
        "id": job.id,
        "title": job.title,
        "company": job.company,
        "location": job.location,
        "work_type": job.work_type,
        "salary": job.salary,
        "skills": job.skills,
        "summary": job.summary,
        "description": job.description,
        "responsibilities": [
            line for line in (job.responsibilities or "").splitlines() if line.strip()
        ],
        "qualifications": [
            line for line in (job.qualifications or "").splitlines() if line.strip()
        ],
        "lat": float(job.lat) if job.lat is not None else None,
        "lng": float(job.lng) if job.lng is not None else None,
        "created_at": job.created_at.isoformat(),
    }

def job_list(request):
    qs = Job.objects.all().order_by("-created_at")
    if request.GET.get("has_location"):
        qs = qs.filter(lat__isnull=False, lng__isnull=False)
    return JsonResponse([_job_to_dict(j) for j in qs], safe=False)

def job_detail(request, pk: int):
    try:
        job = Job.objects.get(pk=pk)
    except Job.DoesNotExist:
        raise Http404("Job not found")
    return JsonResponse(_job_to_dict(job))
