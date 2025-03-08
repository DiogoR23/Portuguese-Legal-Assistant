from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Users, Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id_message', 'id_conversation', 'sender', 'content', 'created_at']


class RegisterSerializer(serializers.ModelSerializer):
    id_user = serializers.UUIDField(format='hex', read_only=True)
    email = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField()
    class Meta:
        model = Users
        fields = ['id_user', 'email', 'username', 'password']

    def create(self, validated_data):
        user = Users.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = Users.objects.filter(email=data["email"]).first()
        if user and user.password == data["password"]:
            refresh = RefreshToken.for_user(user)
            return {"refresh": str(refresh), "access": str(refresh.access_token)}
        raise serializers.ValidationError("Credenciais inválidas.")
