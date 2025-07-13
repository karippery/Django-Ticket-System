from rest_framework import serializers
from .models import Ticket, Comment
from apps.accounts.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'created_at']
        read_only_fields = ['author', 'created_at']


class TicketSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Ticket
        fields = [
            'id', 'title', 'description', 'status', 'priority', 
            'category', 'created_by', 'assigned_to', 'created_at', 
            'updated_at', 'comments'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']


class TicketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'priority', 'category']

    def create(self, validated_data):
        request = self.context.get('request')
        ticket = Ticket.objects.create(
            created_by=request.user,
            **validated_data
        )
        return ticket


class TicketUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['status', 'assigned_to']

    def validate_assigned_to(self, value):
        if value and not (value.is_admin or value.is_agent):
            raise serializers.ValidationError(
                "Can only assign tickets to admins or agents"
            )
        return value
