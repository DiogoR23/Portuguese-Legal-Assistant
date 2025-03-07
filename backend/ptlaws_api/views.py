from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

from .serializers import RegisterSerializer, LoginSerializer, MessageSerializer
from .models import Message, Conversation
from assistant.response import get_ai_response

import datetime

User = get_user_model()

class ChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, conversation_id):
        user_input = request.data.get("message")

        message = Message.objects.create(
            id_conversation=conversation_id,
            sender="user",
            content=user_input,
            created_at=datetime.datetime.utcnow()
        )

        ai_response = get_ai_response(user_input)

        ai_message = Message.objects.create(
            id_conversation=conversation_id,
            sender="AI",
            content=ai_response,
            created_at=datetime.datetime.utcnow()
        )

        return Response({
            "user_message": MessageSerializer(message).data,
            "ai_response": MessageSerializer(ai_message).data
        })

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)
