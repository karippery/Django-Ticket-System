from django.db.models.signals import post_save
from django.dispatch import receiver
from ..tickets.tasks import (
    send_ticket_created_email,
    send_ticket_updated_email,
    send_comment_notification
)
from apps.tickets.models import Ticket, Comment


@receiver(post_save, sender=Ticket)
def ticket_created_handler(sender, instance, created, **kwargs):
    if created:
        send_ticket_created_email.delay(
            instance.id, 
            instance.created_by.email
        )


@receiver(post_save, sender=Ticket)
def ticket_updated_handler(sender, instance, created, **kwargs):
    if not created:
        send_ticket_updated_email.delay(
            instance.id, 
            instance.created_by.email,
            instance.status
        )


@receiver(post_save, sender=Comment)
def comment_created_handler(sender, instance, created, **kwargs):
    if created:
        # Notify ticket creator if comment is from someone else
        if instance.author != instance.ticket.created_by:
            send_comment_notification.delay(
                instance.ticket.id,
                instance.ticket.created_by.email,
                instance.author.username
            )

        # Notify assigned agent if different from comment author and creator
        if (
            instance.ticket.assigned_to != instance.author and
            instance.ticket.assigned_to != instance.ticket.created_by
        ):
            send_comment_notification.delay(
                instance.ticket.id,
                instance.ticket.assigned_to.email,
                instance.author.username
            )
