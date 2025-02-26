from rest_framework import serializers
from .models import Articles, AIAnswers, UserQuestions, Conversations, Users


class ArticlesSerializer(serializers.Serializer):
    class Meta:
        model = Articles
        fields = ['id_articles', 'url', 'title', 'content']


class AIAnswersSerializer(serializers.Serializer):
    class Meta:
        model = AIAnswers
        fields = ['content_answers']


class UserQuestionsSerializer(serializers.Serializer):
    class Meta:
        model = UserQuestions
        fields = ['content_question']


class UsersSerializer(serializers.Serializer):
    class Meta:
        model = Users
        fields = ['name', 'email']

class ConversationSerializer(serializers.Serializer):
    class Meta:
        model = Conversations
        fields = ['id_user', 'data', 'id_question', 'id_answer']