import uuid
from django_cassandra_engine.models import DjangoCassandraModel
from cassandra.cqlengine import columns

# Create your models here.
class Articles(DjangoCassandraModel):
    id_articles = columns.UUID(primary_key=True, default=uuid.uuid4)
    url = columns.Text(required=True)
    title = columns.Text(required=True)
    content = columns.Text(required=True)
    class Meta:
        db_table = 'articles'

class AIAnswers(DjangoCassandraModel):
    id_answers = columns.UUID(primary_key=True, default=uuid.uuid4)
    content_answers = columns.Text(required=True)
    class Meta:
        db_table = 'ai_answers'

class UserQuestions(DjangoCassandraModel):
    id_question = columns.UUID(primary_key=True, default=uuid.uuid4)
    content_question = columns.Text(required=True)
    class Meta:
        db_table = 'user_questions'

class Users(DjangoCassandraModel):
    id_user = columns.UUID(primary_key=True, default=uuid.uuid4)
    name = columns.Text(required=True)
    email = columns.Text(required=True)
    password = columns.Text(required=True)
    class Meta:
        db_table = 'users'

class Conversations(DjangoCassandraModel):
    id_conversation = columns.UUID(primary_key=True, clustering_order='ASC', default=uuid.uuid4)
    id_user = columns.UUID(partition_key=True, required=True)
    date = columns.DateTime(primary_key=True, clustering_order='DESC', required=True)
    id_question = columns.UUID(required=True)
    id_answer = columns.UUID(required=True)
    class Meta:
        db_table = 'conversations'
        get_pk_field = 'id_conversation'
