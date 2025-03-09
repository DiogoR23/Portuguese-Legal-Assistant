from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

from .serializers import RegisterSerializer, UserSerializer, LoginSerializer
from .models import Users

import bcrypt
import jwt
import datetime
import uuid


class RegisterView(APIView):
    """View to register news users."""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            hashed_password = bcrypt.hashpw(serializer.validated_data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            user = Users.create(
                id_user = uuid.uuid4(),
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
        if not user:
            return Response({"error": "Invalid credentials!"}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response({"error": "Invalid credentials!"}, status=status.HTTP_401_UNAUTHORIZED)

        payload = {
            "id_user": str(user.id_user),
            "email": user.email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
            "iat": datetime.datetime.utcnow(),
        }

        access_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        refresh_payload = {
            "id_user": str(user.id_user),
            "email": user.email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
            "iat": datetime.datetime.utcnow(),
        }
        refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm='HS256')

        return Response({
            "message": "Login successful!",
            "access_token": access_token,
            "refresh_token": refresh_token
        }, status=status.HTTP_200_OK)
