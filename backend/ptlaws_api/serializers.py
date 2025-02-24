from rest_framework import serializers

class ArticleSerializer(serializers.Serializer):
    id_article = serializers.UUIDField()
    title = serializers.CharField(max_length=200)
    content = serializers.CharField()
    url = serializers.URLField()


class AnswerSerializer(serializers.Serializer):
    id_anwer = serializers.UUIDField()
    content_answer = serializers.CharField()


class QuestionSerializer(serializers.Serializer):
    id_question = serializers.UUIDField()
    content_question = serializers.CharField()


class ConversationSerializer(serializers.Serializer):
    id_conversation = serializers.UUIDField()
    id_user = serializers.UUIDField()
    id_question = serializers.UUIDField()
    id_answer = serializers.UUIDField()
    date = serializers.DateTimeField()