    
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Avg, Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import Incident, Complaint, Task, KPIValue
from api import models

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def incident_resolution_time(request):
    avg_time = Incident.objects.exclude(resolved_at=None).annotate(
        resolution_time=models.ExpressionWrapper(models.F('resolved_at') - models.F('created_at'), output_field=models.DurationField())
    ).aggregate(avg=models.Avg('resolution_time'))['avg']
    hours = avg_time.total_seconds() / 3600 if avg_time else 0
    return Response({'avg_resolution_hours': round(hours, 2)})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def client_satisfaction(request):
    avg_note = Complaint.objects.aggregate(avg=Avg('satisfaction_note'))['avg'] or 0
    return Response({'avg_satisfaction': round(avg_note, 2)})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def task_completion_rate(request):
    total = Task.objects.count()
    completed = Task.objects.filter(status__label__iexact='Terminé').count()
    rate = (completed / total) * 100 if total else 0
    return Response({'completion_rate': round(rate, 2)})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def incident_response_time(request):
    avg_time = Incident.objects.exclude(first_response_at=None).annotate(
        response_time=models.ExpressionWrapper(models.F('first_response_at') - models.F('created_at'), output_field=models.DurationField())
    ).aggregate(avg=Avg('response_time'))['avg']
    hours = avg_time.total_seconds() / 3600 if avg_time else 0
    return Response({'avg_response_hours': round(hours, 2)})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def incidents_over_time(request):
    period_days = int(request.GET.get('period', 7))
    since = timezone.now() - timedelta(days=period_days)
    data = Incident.objects.filter(created_at__gte=since).extra({'day': "date(created_at)"}).values('day').annotate(count=Count('id')).order_by('day')
    return Response({'data': list(data)})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def tasks_completed_over_time(request):
    period_days = int(request.GET.get('period', 7))
    since = timezone.now() - timedelta(days=period_days)
    data = Task.objects.filter(completed_at__gte=since).extra({'day': "date(completed_at)"}).values('day').annotate(count=Count('id')).order_by('day')
    return Response({'data': list(data)})

