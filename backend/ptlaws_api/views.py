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
from ptlaws_api.helpers.chat import create_conversation_and_first_message

# Import from python
import uuid
from datetime import datetime


class ChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        conversation_id = request.data.get('conversation_id')
        user_message = request.data.get('message')

        if not user_message:
            return Response({'error': 'Message is required.'}, status=status.HTTP_400_BAD_REQUEST)

        if not conversation_id:
            conversation, user_msg = create_conversation_and_first_message(user, user_message)
        else:
            conversation = Conversations.objects.filter(id_conversation=uuid.UUID(conversation_id)).first()
            if not conversation:
                return Response({'error': 'Conversation not found.'}, status=status.HTTP_404_NOT_FOUND)

            user_msg = Message.create(
                id_message=uuid.uuid4(),
                id_conversation=conversation.id_conversation,
                sender='user',
                content=user_message,
                created_at=datetime.utcnow()
            )
            conversation.message_ids.append(user_msg.id_message)

        # AI Response
        ai_response_text = get_ai_response(user_message)
        ai_msg = Message.create(
            id_message=uuid.uuid4(),
            id_conversation=conversation.id_conversation,
            sender='ai',
            content=ai_response_text,
            created_at=datetime.utcnow()
        )
        conversation.message_ids.append(ai_msg.id_message)
        conversation.save()

        return Response({
            'conversation_id': str(conversation.id_conversation),
            'message': [
                MessageSerializer(user_msg).data,
                MessageSerializer(ai_msg).data
            ]
        }, status=status.HTTP_200_OK)



class CreateConversationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        title = request.data.get("title", "")
        conversation = Conversations.create(
            id_conversation=uuid.uuid4(),
            user_id=request.user.user_id,
            title=title,
            created_at=datetime.utcnow(),
            message_ids=[]
        )
        return Response({"conversation_id": str(conversation.id_conversation)}, status=201)


class ListUserConversationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.pk
        conversations = Conversations.objects.filter(user_id=user_id).all()
        serialized = ConversationSerializer(conversations, many=True)

        return Response(serialized.data)


class ListConversationsMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, conversation_id):
        messages = Message.objects.filter(id_conversation=conversation_id).all()
        serialized = MessageSerializer(messages, many=True)

        return Response(serialized.data)
