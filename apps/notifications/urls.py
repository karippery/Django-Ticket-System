from django.urls import path
from .views import NotificationListView, NotificationDetailView

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'),
    path('<int:pk>/',
         NotificationDetailView.as_view(),
         name='notification-detail'
         ),
    path('<int:pk>/mark-read/', NotificationDetailView.as_view(
        http_method_names=['patch']
    ), name='notification-mark-read'),
]