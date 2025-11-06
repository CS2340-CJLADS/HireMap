import csv
import datetime
from django.http import HttpResponse

def export_as_csv(modeladmin, request, queryset):
    """
    A generic admin action to export a queryset to a CSV file.
    Sorts by user, applicant, or recruiter if available, otherwise by PK.
    """
    model = queryset.model
    model_name = model._meta.verbose_name_plural.replace(' ', '-')
    field_names = [field.name for field in model._meta.fields]

    # Determine sorting field
    sort_field = model._meta.pk.name  # Default to PK
    if hasattr(model, 'user') and hasattr(model.user.field.related_model, 'username'):
        sort_field = 'user__username'
    elif hasattr(model, 'applicant') and hasattr(model.applicant.field.related_model, 'user'):
        sort_field = 'applicant__user__username'
    elif hasattr(model, 'recruiter') and hasattr(model.recruiter.field.related_model, 'user'):
        sort_field = 'recruiter__user__username'

    ordered_queryset = queryset.order_by(sort_field)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename=Exported-{model_name}-Data-{datetime.date.today()}.csv'
    writer = csv.writer(response)

    # Write a header row
    writer.writerow(field_names)

    # Write data rows
    for obj in ordered_queryset:
        row = writer.writerow([getattr(obj, field) for field in field_names])

    return response

export_as_csv.short_description = "Export Selected to CSV"

