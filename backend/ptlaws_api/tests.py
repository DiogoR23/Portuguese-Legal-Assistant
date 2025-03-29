from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from users.models import Users
from ptlaws_api.models import Conversations, Message
from django.utils import timezone
import uuid


class ChatViewsTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # Create Users and Tokens
        self.user = Users.objects.create_user(
            email="test@example.com",
            username="TestUser",
            password="testpassword123"
        )

        # Authenticate
        response = self.client.post("/api/users/login/", {
            "email": "test@example.com",
            "password": "testpassword123"
        }, format="json")
        self.access_token = response.data["access_token"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        self.chat_url = "/api/ai/chat/"
        self.create_conversation_url = "/api/ai/create/conversations/"
        self.list_conversations_url = "/api/ai/conversations/"

    def test_create_conversation_manually(self):
        response = self.client.post(self.create_conversation_url, {"title": "Minha Conversa"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("conversation_id", response.data)

    def test_send_message_creates_conversation(self):
        response = self.client.post(self.chat_url, {"message": "Olá AI!"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("conversation_id", response.data)
        self.assertEqual(len(response.data["message"]), 2)

    def test_list_user_conversations(self):
        # Create a conversation manually
        conversation = Conversations.create(
            id_conversation=uuid.uuid4(),
            user_id=self.user.user_id,
            title="Teste Listagem",
            created_at=timezone.now(),
            message_ids=[]
        )

        response = self.client.get(self.list_conversations_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(c["title"] == "Teste Listagem" for c in response.data))

    def test_list_messages_in_conversation(self):
        conversation = Conversations.create(
            id_conversation=uuid.uuid4(),
            user_id=self.user.user_id,
            title="Conversa com Mensagens",
            created_at=timezone.now(),
            message_ids=[]
        )

        msg1 = Message.create(
            id_message=uuid.uuid4(),
            id_conversation=conversation.id_conversation,
            sender="user",
            content="Olá!",
            created_at=timezone.now()
        )
        msg2 = Message.create(
            id_message=uuid.uuid4(),
            id_conversation=conversation.id_conversation,
            sender="ai",
            content="Olá, sou a IA!",
            created_at=timezone.now()
        )
        conversation.message_ids.extend([msg1.id_message, msg2.id_message])
        conversation.save()

        url = f"/api/ai/conversations/{conversation.id_conversation}/messages/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
