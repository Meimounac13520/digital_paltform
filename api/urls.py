
# ---------------------------------------------------------------------------
# Router & URL patterns
# ---------------------------------------------------------------------------

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from api import analytics_views
from api.views import ActionPlanViewSet, ApprovalStepViewSet, AttachmentViewSet, CommentViewSet, ComplaintViewSet, CustomLoginView, DashboardOverviewView, DepartmentViewSet, IncidentViewSet, InternalRequestViewSet, KPIIndicatorViewSet, KPIValueViewSet, KPIViewSet, MilestoneViewSet, NotificationViewSet, ObjectiveViewSet,RoleViewSet,AgencyViewSet,DirectionViewSet, TaskAssignmentViewSet, TaskViewSet,UserViewSet
router = DefaultRouter()
router.register(r'roles', RoleViewSet)
router.register(r'agencies', AgencyViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'directions', DirectionViewSet)
router.register(r'users', UserViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'incidents', IncidentViewSet)
router.register(r'complaints', ComplaintViewSet)
router.register(r'action-plans', ActionPlanViewSet)
router.register(r'objectives', ObjectiveViewSet)
router.register(r'milestones', MilestoneViewSet)
router.register(r'internal-requests', InternalRequestViewSet)
router.register(r'kpi-indicators', KPIIndicatorViewSet)
router.register(r'kpi-values', KPIValueViewSet)
router.register(r'kpi', KPIViewSet)


router.register('task-assignments', TaskAssignmentViewSet)

router.register('approvals', ApprovalStepViewSet)

router.register('notifications', NotificationViewSet)
router.register('comments', CommentViewSet)
router.register('attachments', AttachmentViewSet)
# Expose urlpatterns for inclusion in project urls.py
urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    path('login/',CustomLoginView.as_view(), name='api_token_auth'),
    path('dashboard/overview/', DashboardOverviewView.as_view(), name='dashboard-overview'),
    path('api/analytics/incident-resolution-time/', analytics_views.incident_resolution_time),
    path('api/analytics/client-satisfaction/', analytics_views.client_satisfaction),
    path('api/analytics/task-completion-rate/', analytics_views.task_completion_rate),
    path('api/analytics/incident-response-time/', analytics_views.incident_response_time),
    path('api/analytics/incidents-over-time/', analytics_views.incidents_over_time),
    path('api/analytics/tasks-completed-over-time/', analytics_views.tasks_completed_over_time),
]