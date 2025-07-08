from django_filters.rest_framework import FilterSet, CharFilter, NumberFilter, DateFromToRangeFilter

from .models import (
    Task, Incident, Complaint
)
# ---------------------------------------------------------------------------
# Filters
# ---------------------------------------------------------------------------
class TaskFilter(FilterSet):
    status = CharFilter(field_name='status__code', lookup_expr='iexact')
    agency = NumberFilter(field_name='agency_id')
    due = DateFromToRangeFilter(field_name='due_date')
    class Meta:
        model = Task
        fields = ['status', 'agency', 'due']

class IncidentFilter(FilterSet):
    status = CharFilter(field_name='status__code', lookup_expr='iexact')
    severity = CharFilter(field_name='severity__code', lookup_expr='iexact')
    agency = NumberFilter(field_name='agency_id')
    class Meta:
        model = Incident
        fields = ['status', 'severity', 'agency']

class ComplaintFilter(FilterSet):
    status = CharFilter(field_name='status__code', lookup_expr='iexact')
    channel = CharFilter(field_name='channel__code', lookup_expr='iexact')
    agency = NumberFilter(field_name='agency_id')
    class Meta:
        model = Complaint
        fields = ['status', 'channel', 'agency']