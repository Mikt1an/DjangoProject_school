from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Task


@receiver(pre_save, sender=Task)
def store_previous_task_status(sender, instance, **kwargs):
    if not instance.pk:
        instance._previous_status = None
        return

    try:
        previous_task = (
            sender.objects
            .only("status")
            .get(pk=instance.pk)
        )
        instance._previous_status = previous_task.status

    except sender.DoesNotExist:
        instance._previous_status = None


@receiver(post_save, sender=Task)
def notify_owner_about_status_change(
    sender,
    instance,
    created,
    **kwargs,
):
    if created:
        return

    previous_status = getattr(
        instance,
        "_previous_status",
        None,
    )

    if previous_status is None:
        return

    if previous_status == instance.status:
        return

    if not instance.owner:
        return

    if not instance.owner.email:
        return

    owner_email = instance.owner.email
    task_title = instance.title

    try:
        current_status = instance.get_status_display()
    except AttributeError:
        current_status = instance.status

    subject = f"Task status changed: {task_title}"

    message = (
        f"Hello {instance.owner.username},\n\n"
        f'The status of your task "{task_title}" has changed.\n\n'
        f"Previous status: {previous_status}\n"
        f"Current status: {current_status}\n"
    )

    transaction.on_commit(
        lambda: send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[owner_email],
            fail_silently=False,
        )
    )