from django import template
from django.utils import timezone
from datetime import timedelta

register = template.Library()

@register.filter
def split(value, delimiter=','):
    """Split a string by delimiter and return a list"""
    if not value:
        return []
    return [item.strip() for item in value.split(delimiter) if item.strip()]

@register.filter
def is_recent_timestamp(timestamp):
    """Check if timestamp is recent (within last hour) - likely migration timestamp"""
    if not timestamp:
        return False
    
    now = timezone.now()
    one_hour_ago = now - timedelta(hours=1)
    
    # If timestamp is within the last hour, it's likely from migration
    return timestamp > one_hour_ago

@register.filter
def is_future_timestamp(timestamp):
    """Check if timestamp is in the future"""
    if not timestamp:
        return False
    
    now = timezone.now()
    return timestamp > now
