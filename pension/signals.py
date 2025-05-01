from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.timezone import now
from .models import Room, AuditLog

def create_audit_log(user, action, instance):
    AuditLog.objects.create(
        user=user,
        action=f"{action} {instance.__class__.__name__} - ID {instance.pk}",
        timestamp=now()
    )

def get_instance_user(instance):
    return getattr(instance, "_current_user", None)

@receiver(post_save, sender=Room)
def log_save(sender, instance, created, **kwargs):
    user = get_instance_user(instance)
    action = "Created" if created else "Updated"
    if user:
        create_audit_log(user, action, instance)

@receiver(post_delete, sender=Room)
def log_delete(sender, instance, **kwargs):
    user = get_instance_user(instance)
    if user:
        create_audit_log(user, "Deleted", instance)
