"""
models.py

This module contains the models for the ptlaws_api application.
It defines the data structures for conversations and messages using Django Cassandra Engine.

The models are designed to work with Cassandra as the database backend.
The models include:
- Conversations: Represents a conversation between users.
- Message: Represents a message within a conversation.

Each model is defined as a class that inherits from DjangoCassandraModel.
The models use UUIDs for unique identification and store timestamps for creation.
The Conversations model includes:
- id_conversation: A unique identifier for the conversation (UUID).
- user_id: The ID of the user involved in the conversation (UUID).
- message_ids: A list of message IDs associated with the conversation (List of UUIDs).
- title: The title of the conversation (Text).
- created_at: The timestampes when the conversation was created (DateTime).

The Message model includes:
- id_message: A unique identifier for the message (UUID).
- id_conversation: The ID of the conversation to which the message belongs (UUID).
- sender: The send of the message, if it is a user or an AI (Text).
- content: The content of the message (Text).
- created_at: The timestamp when the message was created (DateTime).

The models are registered with the Django Cassandra Engine and specify the database table names.
"""

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