"""
serializers.py

This module contains the serializers for the Message and Conversation models.
The serializers are used to convert complex data types, such as querysets and model instances, to native Python datatypes that can then be easily rendered into JSON, XML or other content types.
Additionally, they are used to validate incoming data before it is saved to the database.
The MessageSerializer is used to serialize and deserialize Message objects, while the ConversationSerializer is used for Conversation objects.

The serializers are important in:
- Converting complex data types to native Python datatypes.
- Validating incoming data before saving it to the database.
- Providing a way to customize the representation of the data.
- Ensuring that the data is in the correct format for the API responses.

This module is part of the ptlaws_api application, which is a Django REST framework application.
It provides the API for the PT Laws application, which is a legal tech platform that provides legal information and services to users.
The serializers are used in:
- Serializing and deserializing data for the API endpoints.
- Validating incoming data for the API endpoints.
- Customizing the representation of the data for the API responses.

The serializers are used in the views of the ptlaws_api application to handle the data for the API endpoints.
"""

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

    def to_representation(self, instance):
        return {
            "id": str(instance.id_message),
            "conversation_id": str(instance.id_conversation),
            "role": instance.sender,
            "content": instance.content,
            "created_at": instance.created_at.isoformat(),
        }


class ConversationSerializer(serializers.Serializer):
    id_conversation = serializers.UUIDField()
    user_id = serializers.UUIDField()
    message_ids = serializers.ListField()
    title = serializers.CharField()
    created_at = serializers.DateTimeField()
    class Meta:
        model = Conversations
        fields = ['id_conversation', 'user_id', 'message_ids', 'title', 'created_at']