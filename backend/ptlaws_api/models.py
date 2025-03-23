from django_cassandra_engine.models import DjangoCassandraModel
from cassandra.cqlengine import columns

import uuid
import datetime


class Conversations(DjangoCassandraModel):
    id_conversation = columns.UUID(primary_key=True, default=uuid.uuid4)
    user_id = columns.UUID(required=True)
    message_ids = columns.List(columns.UUID)
    title = columns.Text()
    created_at = columns.DateTime(default=datetime.datetime.utcnow)

    class Meta:
        app_label = 'ptlaws_api'
        db_table = "conversations"


class Message(DjangoCassandraModel):
    id_message = columns.UUID(primary_key=True, default=uuid.uuid4)
    id_conversation = columns.UUID(required=True)
    sender = columns.Text(required=True)
    content = columns.Text(required=True)
    created_at = columns.DateTime(default=datetime.datetime.utcnow)

    class Meta:
        app_label = 'ptlaws_api'
        db_table = "messages"