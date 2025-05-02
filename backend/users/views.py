"""
views.py

This module contains the views for user registration, login, and protected routes.
It uses Django REST Framework to handle HTTP requests and responses.
The views are designed to work with the Users model and serializers defined in the same app.

The views include:
- RegisterView: Handles user registration.
- LoginView: Handles user login and token generation.
- ProtectedView: A protected route that requires authentication.

It returns user information if the request is authenticated.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, UserSerializer, LoginSerializer
from .models import Users


class RegisterView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            return Response({
                "user": UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'username': user.username
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        return Response({
            "message": "Welcome to the Protected route!",
            "user": {
                "user_id": str(user.pk),
                "email": user.email,
                "username": user.username
            }
        }, status=status.HTTP_200_OK)
