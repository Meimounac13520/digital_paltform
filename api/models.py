from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Role(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

class Agency(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50)
    location = models.CharField(max_length=255)
    director = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='directed_agencies')

class Direction(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    responsible = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)

class Department(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE)

class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    agency = models.ForeignKey(Agency, on_delete=models.SET_NULL, null=True)

class TaskPriority(models.Model):
    name = models.CharField(max_length=50)
    level = models.IntegerField()

class TaskStatus(models.Model):
    code = models.CharField(max_length=20)
    label = models.CharField(max_length=100)

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    priority = models.ForeignKey(TaskPriority, on_delete=models.SET_NULL, null=True)
    status = models.ForeignKey(TaskStatus, on_delete=models.SET_NULL, null=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)

class TaskAssignment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)

class IncidentSeverity(models.Model):
    code = models.CharField(max_length=20)
    label = models.CharField(max_length=100)

class IncidentStatus(models.Model):
    code = models.CharField(max_length=20)
    label = models.CharField(max_length=100)

class IncidentCategory(models.Model):
    code = models.CharField(max_length=20)
    label = models.CharField(max_length=100)

class Incident(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(IncidentCategory, on_delete=models.SET_NULL, null=True)
    severity = models.ForeignKey(IncidentSeverity, on_delete=models.SET_NULL, null=True)
    status = models.ForeignKey(IncidentStatus, on_delete=models.SET_NULL, null=True)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    reporter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

class ComplaintStatus(models.Model):
    code = models.CharField(max_length=20)
    label = models.CharField(max_length=100)

class ComplaintCategory(models.Model):
    code = models.CharField(max_length=20)
    label = models.CharField(max_length=100)

class ComplaintChannel(models.Model):
    code = models.CharField(max_length=20)
    label = models.CharField(max_length=100)

class Complaint(models.Model):
    reference = models.CharField(max_length=50, unique=True)
    client_name = models.CharField(max_length=255)
    description = models.TextField()
    channel = models.ForeignKey(ComplaintChannel, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(ComplaintCategory, on_delete=models.SET_NULL, null=True)
    status = models.ForeignKey(ComplaintStatus, on_delete=models.SET_NULL, null=True)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)

class ActionPlan(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)

class Objective(models.Model):
    label = models.CharField(max_length=255)
    target_value = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50)
    due_date = models.DateField()
    status = models.CharField(max_length=50)
    action_plan = models.ForeignKey(ActionPlan, on_delete=models.CASCADE)

class Milestone(models.Model):
    label = models.CharField(max_length=255)
    due_date = models.DateField()
    completed_on = models.DateField(null=True, blank=True)
    objective = models.ForeignKey(Objective, on_delete=models.CASCADE)

class InternalRequest(models.Model):
    subject = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    requester = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)

class ApprovalStep(models.Model):
    request = models.ForeignKey(InternalRequest, on_delete=models.CASCADE)
    approver_role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    decision = models.CharField(max_length=50)
    decided_at = models.DateTimeField(null=True, blank=True)
    comment = models.TextField(blank=True)

class KPIIndicator(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    formula = models.TextField(blank=True)

class KPIValue(models.Model):
    indicator = models.ForeignKey(KPIIndicator, on_delete=models.CASCADE)
    period = models.CharField(max_length=20)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    calculated_at = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    seen = models.BooleanField(default=False)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    related_object = GenericForeignKey('content_type', 'object_id')

class Attachment(models.Model):
    file = models.FileField(upload_to='attachments/')
    original_name = models.CharField(max_length=255)
    mime_type = models.CharField(max_length=100)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    related_object = GenericForeignKey('content_type', 'object_id')
