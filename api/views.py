
# Create your views here.

from rest_framework.decorators import action
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.filters import ComplaintFilter, IncidentFilter, TaskFilter
from api.permissions import IsAdmin, IsAdminOrReadOnly, IsDirectorOrReadOnly, IsSameAgencyOrAdmin
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import (
    ApprovalStep, Attachment, Notification, Role, Agency, Department, Direction, TaskAssignment, User,
    Task, Incident, Complaint,
    ActionPlan, Objective, Milestone,
    InternalRequest, KPIIndicator, KPIValue,Comment
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import (
    ApprovalStepSerializer, AttachmentSerializer, CommentSerializer, NotificationSerializer, RoleSerializer, AgencySerializer, DepartmentSerializer, DirectionSerializer, TaskAssignmentSerializer, UserSerializer,
    TaskSerializer, IncidentSerializer, ComplaintSerializer,
    ActionPlanSerializer, ObjectiveSerializer, MilestoneSerializer,
    InternalRequestSerializer, KPIIndicatorSerializer, KPIValueSerializer
)

class CustomLoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.user  # <- pas `validated_data['user']` ici
        user_data = UserSerializer(user).data
        return Response({
            'access': serializer.validated_data['access'],
            'refresh': serializer.validated_data['refresh'],
            'user': user_data
        })
# ---------------------------------------------------------------------------
# Generic base viewset for simple lookups
# ---------------------------------------------------------------------------
class LookupModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'label', 'code']
    ordering_fields = ['name', 'label', 'code']

# ---------------------------------------------------------------------------
# ViewSets
# ---------------------------------------------------------------------------
# ViewSets
class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAdmin]

class AgencyViewSet(viewsets.ModelViewSet):
    queryset = Agency.objects.all()
    serializer_class = AgencySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['type']
    search_fields = ['name']
    permission_classes = [IsAdmin | IsDirectorOrReadOnly]

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAdmin]

class DirectionViewSet(viewsets.ModelViewSet):
    queryset = Direction.objects.all()
    serializer_class = DirectionSerializer
    permission_classes = [IsAdmin]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['role', 'agency']
    search_fields = ['username', 'first_name', 'last_name']
    permission_classes = [IsAdmin]

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'priority', 'agency']
    search_fields = ['title']
    permission_classes = [permissions.IsAuthenticated]
    @action(detail=False, methods=['get'])
    def in_progress(self, request):
        tasks = self.queryset.exclude(status__label__iexact='Terminé')
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

class TaskAssignmentViewSet(viewsets.ModelViewSet):
    queryset = TaskAssignment.objects.all()
    serializer_class = TaskAssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]

class IncidentViewSet(viewsets.ModelViewSet):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'severity', 'category', 'agency']
    permission_classes = [permissions.IsAuthenticated]
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def open(self, request):
        incidents = self.queryset.exclude(status__label__iexact='Clôturé')
        serializer = self.get_serializer(incidents, many=True)
        return Response(serializer.data)

class ComplaintViewSet(viewsets.ModelViewSet):
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'category', 'channel', 'agency']
    permission_classes = [permissions.IsAuthenticated]
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def open(self, request):
        complaints = self.queryset.exclude(status__label__iexact='Clôturé')
        serializer = self.get_serializer(complaints, many=True)
        return Response(serializer.data)

class ActionPlanViewSet(viewsets.ModelViewSet):
    queryset = ActionPlan.objects.all()
    serializer_class = ActionPlanSerializer
    permission_classes = [IsDirectorOrReadOnly]
    @action(detail=False, methods=['get'])
    def active(self, request):
        plans = self.queryset.filter(status__iexact='Actif')
        serializer = self.get_serializer(plans, many=True)
        return Response(serializer.data)

class ObjectiveViewSet(viewsets.ModelViewSet):
    queryset = Objective.objects.all()
    serializer_class = ObjectiveSerializer
    permission_classes = [IsDirectorOrReadOnly]

class MilestoneViewSet(viewsets.ModelViewSet):
    queryset = Milestone.objects.all()
    serializer_class = MilestoneSerializer
    permission_classes = [IsDirectorOrReadOnly]

class InternalRequestViewSet(viewsets.ModelViewSet):
    queryset = InternalRequest.objects.all()
    serializer_class = InternalRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

class ApprovalStepViewSet(viewsets.ModelViewSet):
    queryset = ApprovalStep.objects.all()
    serializer_class = ApprovalStepSerializer
    permission_classes = [IsDirectorOrReadOnly]

class KPIIndicatorViewSet(viewsets.ModelViewSet):
    queryset = KPIIndicator.objects.all()
    serializer_class = KPIIndicatorSerializer
    permission_classes = [IsAdmin | IsDirectorOrReadOnly]

class KPIValueViewSet(viewsets.ModelViewSet):
    queryset = KPIValue.objects.all()
    serializer_class = KPIValueSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['indicator', 'period']
    permission_classes = [permissions.IsAuthenticated]

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['recipient', 'seen']
    permission_classes = [permissions.IsAuthenticated]

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    permission_classes = [permissions.IsAuthenticated]



############################################1. API DashboardOverviewView###############################################
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ActionPlan, Task, Incident, Complaint, KPIValue

class DashboardOverviewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = {
            "active_action_plans": ActionPlan.objects.filter(status='active').count(),
            "open_tasks": Task.objects.filter(status__code='open').count(),
            "open_incidents": Incident.objects.filter(status__code='open').count(),
            "open_complaints": Complaint.objects.filter(status__code='in_treatment').count(),
            "connection_rate": 94.0,  # à calculer selon logique agence
            "global_performance": KPIValue.objects.filter(indicator__code='global_perf').last().value,
            "revenue": 2800000000,  # À intégrer avec un modèle "FinanceKPI" si besoin
            "transactions_per_day": 15420  # Idem
        }
        return Response(data)
from datetime import timedelta
from django.utils.timezone import now
from django.db.models import Avg, Count, Q, F, ExpressionWrapper, DurationField
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Incident, Complaint, Task, KPIValue

class AnalyticsOverviewView(APIView):
    permission_classes = [IsAuthenticated]

    PERIOD_MAPPING = {
        '24h': timedelta(days=1),
        '7d': timedelta(days=7),
        '30d': timedelta(days=30),
        '3m': timedelta(days=90),
    }

    def get(self, request):
        period = request.GET.get('period', '7d')
        delta = self.PERIOD_MAPPING.get(period, timedelta(days=7))
        start_date = now() - delta

        # 1. Durée moyenne de résolution incidents (en heures)
        incidents = Incident.objects.filter(created_at__gte=start_date, resolved_at__isnull=False)
        avg_resolution = incidents.annotate(
            resolution_time=ExpressionWrapper(F('resolved_at') - F('created_at'), output_field=DurationField())
        ).aggregate(avg=Avg('resolution_time'))['avg']
        resolution_hours = round(avg_resolution.total_seconds() / 3600, 1) if avg_resolution else 0

        # 2. Satisfaction Client (note moyenne des réclamations)
        avg_satisfaction = Complaint.objects.filter(created_at__gte=start_date, satisfaction_note__isnull=False).aggregate(avg=Avg('satisfaction_note'))['avg'] or 0

        # 3. Taux de complétion (tâches terminées / total)
        total_tasks = Task.objects.filter(created_at__gte=start_date).count()
        completed_tasks = Task.objects.filter(created_at__gte=start_date, status__code='completed').count()
        completion_rate = round((completed_tasks / total_tasks) * 100, 1) if total_tasks else 0

        # 4. Temps moyen de réponse incidents
        avg_response = Incident.objects.filter(created_at__gte=start_date, first_response_at__isnull=False).annotate(
            response_time=ExpressionWrapper(F('first_response_at') - F('created_at'), output_field=DurationField())
        ).aggregate(avg=Avg('response_time'))['avg']
        response_hours = round(avg_response.total_seconds() / 3600, 1) if avg_response else 0

        # 5. Evolution des incidents par jour
        incidents_per_day = [
            Incident.objects.filter(created_at__date=now().date() - timedelta(days=i)).count()
            for i in reversed(range(delta.days))
        ]

        # 6. Tâches complétées par jour
        tasks_per_day = [
            Task.objects.filter(completed_at__date=now().date() - timedelta(days=i)).count()
            for i in reversed(range(delta.days))
        ]

        # 7. Performance Globale par jour
        perf_per_day = [
            KPIValue.objects.filter(indicator__code='global_perf', period=(now().date() - timedelta(days=i)).isoformat()).values_list('value', flat=True).first() or 0
            for i in reversed(range(delta.days))
        ]

        data = {
            "incident_resolution_time": resolution_hours,
            "client_satisfaction": round(avg_satisfaction, 1),
            "completion_rate": completion_rate,
            "response_time": response_hours,
            "incidents_per_day": incidents_per_day,
            "tasks_completed_per_day": tasks_per_day,
            "performance_global_per_day": perf_per_day
        }

        return Response(data)


class KPIViewSet(viewsets.ViewSet):
    queryset=KPIValue.objects.all()
    def get_queryset(self):
        return super().get_queryset()
    
    def list(self, request):
        indicator_code = request.query_params.get('indicator', None)
        if indicator_code:
            kpis = KPIValue.objects.filter(indicator__code=indicator_code).order_by('-calculated_at')[:1]
        else:
            kpis = KPIValue.objects.all().order_by('-calculated_at')[:10]
        serializer = KPIValueSerializer(kpis, many=True)
        return Response(serializer.data)