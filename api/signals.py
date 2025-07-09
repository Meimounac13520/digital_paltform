from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.timezone import now
from .models import Task, Incident

# Pour les tâches : fixer completed_at automatiquement quand status = 'completed'
@receiver(pre_save, sender=Task)
def set_task_completed_at(sender, instance, **kwargs):
    if instance.status and instance.status.code == 'completed':
        if not instance.completed_at:
            instance.completed_at = now()
    else:
        instance.completed_at = None  # Si on repasse en mode ouvert, on efface la date

# Pour les incidents : fixer first_response_at automatiquement au premier passage en 'in_progress'
@receiver(pre_save, sender=Incident)
def set_incident_response_and_resolution(sender, instance, **kwargs):
    if instance.status and instance.status.code == 'in_progress':
        if not instance.first_response_at:
            instance.first_response_at = now()
    elif instance.status and instance.status.code == 'resolved':
        if not instance.resolved_at:
            instance.resolved_at = now()
