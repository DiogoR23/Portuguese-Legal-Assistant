from django_cassandra_engine.models import DjangoCassandraModel
from cassandra.cqlengine import columns
import uuid
import datetime
import bcrypt

class Conversations(DjangoCassandraModel):
    id_conversation = columns.UUID(primary_key=True, default=uuid.uuid4)
    id_user = columns.UUID(required=True)
    message_ids = columns.List(columns.UUID)
    title = columns.Text()
    created_at = columns.DateTime(default=datetime.datetime.utcnow)

    class Meta:
        db_table = "conversations"

class Message(DjangoCassandraModel):
    id_message = columns.UUID(primary_key=True, default=uuid.uuid4)
    id_conversation = columns.UUID(required=True)
    sender = columns.Text(required=True)
    content = columns.Text(required=True)
    created_at = columns.DateTime(default=datetime.datetime.utcnow)

    class Meta:
        db_table = "messages"

class Users(DjangoCassandraModel):
    id_user = columns.UUID(primary_key=True, default=uuid.uuid4)
    email = columns.Text(required=True, index=True)
    username = columns.Text(required=True, index=True)
    password = columns.Text(required=True)

    is_active = columns.Boolean(default=True)
    is_staff = columns.Boolean(default=False)
    is_superuser = columns.Boolean(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']

    class Meta:
        db_table = 'users'

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

