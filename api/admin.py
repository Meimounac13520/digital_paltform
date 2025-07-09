from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *

admin.site.register(Role)
admin.site.register(Agency)
admin.site.register(User)
admin.site.register(Direction)
admin.site.register(Department)
admin.site.register(TaskPriority)
admin.site.register(TaskStatus)
admin.site.register(Task)
admin.site.register(TaskAssignment)
admin.site.register(IncidentSeverity)
admin.site.register(IncidentStatus)
admin.site.register(IncidentCategory)
admin.site.register(Incident)
admin.site.register(ComplaintStatus)
admin.site.register(ComplaintCategory)
admin.site.register(ComplaintChannel)
admin.site.register(Complaint)
admin.site.register(ActionPlan)
admin.site.register(Objective)
admin.site.register(Milestone)
admin.site.register(InternalRequest)
admin.site.register(ApprovalStep)
admin.site.register(KPIIndicator)
admin.site.register(KPIValue)
admin.site.register(Notification)
admin.site.register(Comment)
admin.site.register(Attachment)
