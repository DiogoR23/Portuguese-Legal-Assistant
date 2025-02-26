from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Articles, AIAnswers, UserQuestions, Conversations, Users
from .serializers import ArticlesSerializer, ConversationSerializer, UserQuestionsSerializer, AIAnswersSerializer, UsersSerializer
from assistant.response import get_ai_response

class ListUserView(APIView):
    """
    View to list all the users, only admins are able to access.
    """

    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        """
        Return all the users.
        """
        users = Users.objects.all()
        serializer = UsersSerializer(users, many=True)
        return Response(serializer.data)

class CreateUserView(APIView):
    """
    View to create a new User.
    """
    def post(self, request, format=None):
        """
        Create a new User.
        """
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AIResponseView(APIView):
    """
    View to get the AI response and the articles that the RAG chose.
    """
    def get(self, request, format=None):
        user_input = request.query_params.get('question')

        ai_response = get_ai_response(user_input=user_input)

        return Response({'ai_response': ai_response})