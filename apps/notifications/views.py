from rest_framework import generics, permissions
from .models import Notification
from .serializers import NotificationSerializer
from django_filters.rest_framework import DjangoFilterBackend


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_read', 'notification_type']

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


class NotificationDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
