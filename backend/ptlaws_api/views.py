# Importing from Django
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings

from assistant.response import get_ai_response


class ChatView(APIView):
    """Public Endpoint for sending messages to the chatbot."""
    permission_classes = [AllowAny] # Without Authentication

    def post(self, request):
        user_message = request.data.get("message", "")

        ai_reponse = get_ai_response(user_input=user_message)

        return Response({"response": ai_reponse})
