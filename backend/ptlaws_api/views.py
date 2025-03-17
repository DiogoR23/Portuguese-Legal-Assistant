# Importing from Django
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings

# Importing from local folders
from .serializers import RegisterSerializer, UserSerializer, LoginSerializer
from .models import Users
from assistant.response import get_ai_response

# importing from Python
import bcrypt
import jwt
import datetime
import uuid


class ChatView(APIView):
    """Public Endpoint for sending messages to the chatbot."""
    permission_classes = [AllowAny] # Without Authentication

    def post(self, request):
        user_message = request.data.get("message", "")

        ai_reponse = get_ai_response(user_input=user_message)

        return Response({"response": ai_reponse})


class ProtectedView(APIView):
    """Protected Route for testing authentication"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "You have access!"}, status=status.HTTP_200_OK)

class RegisterView(APIView):
    """View to register news users."""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            hashed_password = bcrypt.hashpw(serializer.validated_data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            user = Users.create(
                id = uuid.uuid4(),
                email = serializer.validated_data['email'].lower(),
                username = serializer.validated_data['username'],
                password = hashed_password
            )

            return Response({"message": "User registered successfully!", "user": UserSerializer(user).data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    """View to login and obtain JWT token."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = Users.objects.filter(email=email).first()
        if not user or not user.check_password(password):
            return Response({"error": "Invalid credentials!"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        refresh['user_id'] = str(user.id)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return Response({
            "message": "Login successful!",
            "access_token": access_token,
            "refresh_token": refresh_token
        }, status=status.HTTP_200_OK)

