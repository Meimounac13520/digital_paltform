
# ---------------------------------------------------------------------------
# Router & URL patterns
# ---------------------------------------------------------------------------

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from api.views import ActionPlanViewSet, ApprovalStepViewSet, AttachmentViewSet, CommentViewSet, ComplaintViewSet, CustomLoginView, DepartmentViewSet, IncidentViewSet, InternalRequestViewSet, KPIIndicatorViewSet, KPIValueViewSet, MilestoneViewSet, NotificationViewSet, ObjectiveViewSet,RoleViewSet,AgencyViewSet,DirectionViewSet, TaskAssignmentViewSet, TaskViewSet,UserViewSet
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

router.register('task-assignments', TaskAssignmentViewSet)

router.register('approvals', ApprovalStepViewSet)

router.register('notifications', NotificationViewSet)
router.register('comments', CommentViewSet)
router.register('attachments', AttachmentViewSet)
# Expose urlpatterns for inclusion in project urls.py
urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    path('login/',CustomLoginView.as_view(), name='api_token_auth')
]