from django import template
from django.utils import timezone
from django.utils.dateformat import format
import pytz

register = template.Library()

@register.filter
def local_time(value):
    """
    Convert a datetime to the user's local timezone
    """
    if not value:
        return value
    
    # If the datetime is naive, make it timezone aware
    if timezone.is_naive(value):
        value = timezone.make_aware(value)
    
    # Convert to local timezone
    local_tz = timezone.get_current_timezone()
    return value.astimezone(local_tz)

@register.filter
def format_local_time(value, format_string="g:i A"):
    """
    Format a datetime in the user's local timezone
    """
    if not value:
        return value
    
    local_time_value = local_time(value)
    return format(local_time_value, format_string)
