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

def index(request, user_id):
    session = connect_to_cassandra()

    

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


class CreateConversationView(APIView):
    def post(self, request, *args, **kwargs):
        # Connect to Cassandra Database
        session = connect_to_cassandra()

        # Get users questions
        user_question = request.data.get('question')
        user_id = request.data.get('user_id')
        
        # Generate a new unique ID for each question and answer
        id_question = uuid4()
        id_answer = uuid4()

        if not user_id or not user_question:
            return Response({"error": "id_user and content_questions are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Get the AI response
        ai_response = get_ai_response(user_input=user_question)

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
        session.execute(answer_query, (id_answer, ai_response))

        # Insert in the conversations table
        id_conversation = uuid4()
        date = datetime.datetime.now()

        conversation_query = """
            INSERT INTO conversations (id_conversation, id_user, id_question, id_answer, date)
            VALUES (%s, %s, %s, %s, %s)
        """
        session.execute(conversation_query, (id_conversation, user_id, id_question, id_answer, date))

        return Response({"id_conversations": id_conversation, "answer": ai_response}, status=status.HTTP_201_CREATED)

class GetConversationView(APIView):
    def get(self, request, user_id):
        session = connect_to_cassandra()

        query_answer = "SELECT id_answer FROM conversations WHERE id_user=%s"
        answers_id = session.execute(query_answer, (user_id))

        query_question = "SELECT id_question FROM conversations WHERE id_user=%s"
        questions_id = session.execute(query_question, (user_id))

        for answer_id in answers_id:
            query_content_answer = "SELECT content_answers FROM ai_answers WHERE id_answers=%s"
            questions_content = session.execute(query_content_answer, (answer_id))
        
        for question_id in questions_id:
            query_content_questions = "SELECT content_question FROM user_questions WHERE id_question=%s"
            questions_content = session.execute(query_content_questions, (question_id))

        query = "SELECT id_conversation, date FROM conversations WHERE id_user=%s"
        rows = session.execute(query, (user_id))

        conversations = [
            {
                "id_conversations": str(row.id_conversation),
                "date": row.date,
                "question_content": question,
                "answer_content": answer
            }
            for row, question, answer in zip(rows, questions_content, questions_content)
        ]

        return Response(conversations, status=status.HTTP_200_OK)









