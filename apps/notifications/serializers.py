from rest_framework import serializers
from .models import Notification
from apps.accounts.serializers import UserSerializer
from apps.tickets.serializers import TicketSerializer


class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    ticket = TicketSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'user', 'ticket', 'message',
                  'notification_type', 'is_read', 'created_at']
        read_only_fields = ['user', 'ticket', 'created_at']
