from rest_framework import serializers

from .models import Message, Conversations

class MessageSerializer(serializers.Serializer):
    id_message = serializers.UUIDField()
    id_conversation = serializers.UUIDField()
    sender = serializers.CharField()
    content = serializers.CharField()
    created_at = serializers.DateTimeField()
    class Meta:
        model = Message
        fields = ['id_message', 'id_conversation', 'sender', 'content', 'created_at']


class ConversationSerializer(serializers.Serializer):
    id_conversation = serializers.UUIDField()
    user_id = serializers.UUIDField()
    message_ids = serializers.ListField()
    title = serializers.CharField()
    created_at = serializers.DateTimeField()
    class Meta:
        model = Conversations
        fields = ['id_conversation', 'user_id', 'message_ids', 'title', 'created_at']