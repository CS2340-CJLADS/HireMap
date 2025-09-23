from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


def applicant_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped(request, *args, **kwargs):
        if hasattr(request.user, 'applicant'):
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("Applicants only.")
    return _wrapped


def recruiter_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped(request, *args, **kwargs):
        if hasattr(request.user, 'recruiter'):
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("Recruiters only.")
    return _wrapped


