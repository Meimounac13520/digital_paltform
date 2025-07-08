from rest_framework import serializers
from .models import (
    Role, Agency, Department, Direction, User, TaskPriority, TaskStatus, Task, TaskAssignment,
    IncidentSeverity, IncidentStatus, IncidentCategory, Incident,
    ComplaintStatus, ComplaintCategory, ComplaintChannel, Complaint,
    ActionPlan, Objective, Milestone,
    InternalRequest, ApprovalStep,
    KPIIndicator, KPIValue, Notification, Comment, Attachment
)

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class DirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direction
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class TaskPrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskPriority
        fields = '__all__'

class TaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStatus
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class TaskAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskAssignment
        fields = '__all__'

class IncidentSeveritySerializer(serializers.ModelSerializer):
    class Meta:
        model = IncidentSeverity
        fields = '__all__'

class IncidentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncidentStatus
        fields = '__all__'

class IncidentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = IncidentCategory
        fields = '__all__'

class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = '__all__'

class ComplaintStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplaintStatus
        fields = '__all__'

class ComplaintCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplaintCategory
        fields = '__all__'

class ComplaintChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplaintChannel
        fields = '__all__'

class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = '__all__'

class ActionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActionPlan
        fields = '__all__'

class ObjectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Objective
        fields = '__all__'

class MilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milestone
        fields = '__all__'

class InternalRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternalRequest
        fields = '__all__'

class ApprovalStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalStep
        fields = '__all__'

class KPIIndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = KPIIndicator
        fields = '__all__'

class KPIValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = KPIValue
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = '__all__'
