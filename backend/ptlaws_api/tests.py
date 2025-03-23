from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse

from users.models import Users

# Create your tests here.
class ChatTests(APITestCase):
    def setUp(self):
        self.client_api = APIClient()
        self.chat_url = "/api/ai/chat/"
        
        # Create User
        self.user = Users.objects.create_user(
            email = "chatuser@example.com",
            username = "Chatuser",
            password = "securepass123"
        )
        
        # Authenticate and obtain token
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        # Authenticate Client
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def test_chat_api_returns_ai_response(self):
        """
        Test if the chat API answers correctly to a valid message.
        """

        payload = {
            "message": "Olá, qual a capital de Portugal?"
        }

        response = self.client.post(self.chat_url, data=payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("conversation_id", response.data)
        self.assertIn("message", response.data)

        messages = response.data['message']
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]['sender'], 'user')
        self.assertEqual(messages[1]['sender'], 'ai')