"""
views.py

This file contains the views for the chat application. It includes the following views:
1. ChatView: Handles the chat functionality, including sending and receiving messages.
2. CreateConversationView: Handles the creation of new conversations.
3. ListUserConversationsView: Lists all conversations for a user.
4. ListConversationsMessagesView: Lists all messages in a specific conversation.
5. DeleteConversationView: Deletes a specific conversation.
6. UpdateConversationTitleView: Updates the title of a specific conversation.

Each view is implemented as a class-based view using Django REST Framework's APIView. The views handle HTTP requests and responses, including validation of input data and error handling.
The views use serializers to convert model instances to JSON format and vice versa. The views also use Django's built-in permissions to restrict access to authenticated users only.
They inteact with the database using Django's ORM to create, retrieve, update, and delete conversation and message records.
"""

# Importing from Django
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

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
                MessageSerializer(ai_msg).data,
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

class DeleteConversationView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, conversation_id):
        conversation = Conversations.objects.filter(id_conversation=conversation_id, user_id=request.user.pk).first()

        if not conversation:
            return Response({'error': 'Conversation not Found'}, status=status.HTTP_404_NOT_FOUND)
        
        conversation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UpdateConversationTitleView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, conversation_id):
        new_title = request.data.get('title', '').strip()
        if not new_title:
            return Response({'error': 'Title is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        conversation = Conversations.objects.filter(id_conversation=conversation_id, user_id=request.user.pk).first()
        if not conversation:
            return Response({'error': 'Conversation not Found.'}, status=status.HTTP_404_NOT_FOUND)
        
        conversation.title = new_title
        conversation.save()

        return Response({'message': 'Title updated successfully.'}, status=status.HTTP_200_OK)

