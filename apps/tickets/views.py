from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Ticket
from .serializers import (
    TicketSerializer,
    TicketCreateSerializer,
    TicketUpdateSerializer,
    CommentSerializer
)
from rest_framework.response import Response


class TicketListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
        ]
    filterset_fields = ['status', 'priority', 'category']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'priority']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TicketCreateSerializer
        return TicketSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_admin or user.is_agent:
            return Ticket.objects.all()
        return Ticket.objects.filter(created_by=user)


class TicketDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return TicketUpdateSerializer
        return TicketSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_admin or user.is_agent:
            return Ticket.objects.all()
        return Ticket.objects.filter(created_by=user)


class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        ticket_id = self.kwargs.get('ticket_id')
        ticket = generics.get_object_or_404(Ticket, id=ticket_id)
        serializer.save(ticket=ticket, author=self.request.user)


class DashboardStatsView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        stats = {}

        if user.is_admin or user.is_agent:
            stats['total_tickets'] = Ticket.objects.count()
            stats['open_tickets'] = Ticket.objects.filter(
                status='open').count()
            stats['in_progress_tickets'] = (
                Ticket.objects.filter(
                    status='in_progress'
                ).count()
            )
            stats['closed_tickets'] = Ticket.objects.filter(
                status='closed').count()
        else:
            stats['total_tickets'] = Ticket.objects.filter(
                created_by=user).count()
            stats['open_tickets'] = Ticket.objects.filter(
                created_by=user, status='open').count()
            stats['in_progress_tickets'] = Ticket.objects.filter(
                created_by=user, status='in_progress').count()
            stats['closed_tickets'] = Ticket.objects.filter(
                created_by=user, status='closed').count()

        return Response(stats)
