from rest_framework import serializers
import bcrypt

from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id_message', 'id_conversation', 'sender', 'content', 'created_at']