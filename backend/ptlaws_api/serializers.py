from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import bcrypt

from .models import Users, Message

import uuid

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id_message', 'id_conversation', 'sender', 'content', 'created_at']

class UserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format='hex_verbose')
    email = serializers.CharField()
    username = serializers.CharField()

    is_active = serializers.BooleanField()
    is_staff = serializers.BooleanField()
    is_superuser = serializers.BooleanField() 
    class Meta:
        model = Users
        fields = ['id', 'email', 'username', 'is_active', 'is_staff', 'is_superuser']

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        if Users.objects.filter(email=value).count() > 0:
            raise serializers.ValidationError("This email is already in use.")
        return value

    def validate_username(self, value):
        if Users.objects.filter(username=value).count() > 0:
            raise serializers.ValidationError("This username is already in use.")
        return value

    def create(self, validated_data):
        """Create a user and encrypt the password before saving"""
        hashed_password = bcrypt.hashpw(validated_data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        user = Users.create(
            id=uuid.uuid4(),
            email=validated_data['email'].lower(),
            username=validated_data['username'],
            password=hashed_password
        )

        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = Users.objects.filter(email=email).first()

        if not user:
            raise ValueError("Invalid email or password!")

        if not user.password or not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            raise serializers.ValidationError("Invalid email or password!")

        data['user'] = user

        return data