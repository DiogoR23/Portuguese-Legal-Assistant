from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from uuid import uuid4
import datetime
from .serializers import ArticleSerializer, ConversationSerializer, QuestionSerializer, AnswerSerializer
from assistant.database import connect_to_cassandra
from assistant.response import get_ai_response
import os
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("CASSANDRA_USERNAME")
password = os.getenv("CASSANDRA_PASSWORD")

class ArticleView(APIView):
    def get(self, request, *args, **kwargs):
        # Connect to Cassandra Database
        session = connect_to_cassandra()

        # Query in the articles table
        query = "SELECT * FROM articles WHERE id_article = %s"
        rows = session.execute(query, [kwargs['id_article']])

        articles = []
        for row in rows:
            articles.append({
                'id_article': row['id_articles'],
                'url': row['url'],
                'title': row['title'],
                'content': row['content']
            })

        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ConversationView(APIView):
    def psot(self, request, *args, **kwargs):
        # Connect to Cassandra Database
        session = connect_to_cassandra()

        # Get users questions
        user_question = request.data.get('question')
        user_id = request.data.get('user_id')
        
        # Generate a new unique ID for each question and answer
        id_question = uuid4()
        id_answer = uuid4()

        # Get the AI response
        response = get_ai_response(user_input=user_question)

        # Insert the question in the user_questions table
        question_query = """
            INSERT INTO user_questions (id_question, content_question)
            VALUES (%s, %s)
        """
        session.execute(question_query, (id_question, user_question))

        # Insert the AI response in the ai_answers table
        answer_query = """
            INSERT INTO ai_answers (id_answers, content_answers)
            VALUES (%s, %s)
        """
        session.execute(answer_query, (id_answer, response))

        # Insert in the conversations table
        id_conversation = uuid4()
        date = datetime.datetime.now()

        conversation_query = """
            INSERT INTO conversations (id_conversation, id_user, id_question, id_answer, date)
            VALUES (%s, %s, %s, %s, %s)
        """
        session.execute(conversation_query, (id_conversation, user_id, id_question, id_answer, date))

        return Response({"message": "Conversation recorded successfully!"}, status=status.HTTP_201_CREATED)







