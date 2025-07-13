from django.urls import path
from .views import (
    TicketListView,
    TicketDetailView,
    CommentCreateView,
    DashboardStatsView
    )

urlpatterns = [
    path('', TicketListView.as_view(), name='ticket-list'),
    path('<int:pk>/', TicketDetailView.as_view(), name='ticket-detail'),
    path('<int:ticket_id>/comments/',
         CommentCreateView.as_view(),
         name='comment-create'
         ),
    path('stats/', DashboardStatsView.as_view(), name='ticket-stats'),
]