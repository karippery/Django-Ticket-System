from django.db import models
from django.contrib.auth import get_user_model
from apps.tickets.models import Ticket

User = get_user_model()


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('ticket_created', 'Ticket Created'),
        ('ticket_updated', 'Ticket Updated'),
        ('comment_added', 'Comment Added'),
        ('status_changed', 'Status Changed'),
    )

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='notifications'
                             )
    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE,
        null=True,
        blank=True
        )
    message = models.TextField()
    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES
        )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        app_label = 'notifications'

    def __str__(self):
        return f"{self.user.email} - {self.notification_type}"
