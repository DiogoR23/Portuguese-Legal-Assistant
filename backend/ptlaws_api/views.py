# Importing from Django
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

# Importing from local files
from assistant.response import get_ai_response
from .serializers import ConversationSerializer, MessageSerializer
from .models import Conversations, Message

# Import from python
import uuid
from datetime import datetime


class ChatView(APIView):
    """Public Endpoint for sending messages to the chatbot."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        conversation_id = request.data.get('conversation_id')
        user_message = request.data.get('message')

        if not user_message:
            return Response({'error': 'Message is Required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new conversation if the is no ID 
        if not conversation_id:
            conversation = Conversations.create(
                id_conversation = uuid.uuid4(),
                user_id = user.pk,
                title = "New conversation",
                message_ids = [],
                created_at = datetime.utcnow()
            )
        else:
            conversation = Conversations.objects.filter(id_conversation=uuid.UUID(conversation_id)).first()
            if not conversation:
                return Response({'Error': 'Conversation not Found.'}, status=status.HTTP_404_NOT_FOUND)

        # User Message
        user_msg = Message.create(
            id_message = uuid.uuid4(),
            id_conversation = conversation.id_conversation,
            sender = 'user',
            content = user_message,
            created_at = datetime.utcnow()
        )
        conversation.message_ids.append(user_msg.id_message)

        # AI Response
        ai_response_text = get_ai_response(user_message)
        ai_msg = Message.create(
            id_message = uuid.uuid4(),
            id_conversation = conversation.id_conversation,
            sender = 'ai',
            content = ai_response_text,
            created_at = datetime.utcnow()
        )
        conversation.message_ids.append(ai_msg.id_message)

        # Update conversation with new messages
        conversation.save()

        return Response({
            'conversation_id': str(conversation.id_conversation),
            'message': [
                MessageSerializer(user_msg).data,
                MessageSerializer(ai_msg).data
            ]
        }, status=status.HTTP_200_OK)
