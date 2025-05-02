"""
chat.py

This module contains helper functions for managing chat conversations and messages.
It includes functions to create a new conversation and its first message, as well as to generate a title for the conversation based on the user's message.

Functions:
- create_conversation_and_first_message(): Creates a new conversation and its first message.
- generate_title(): Generates a title for the conversation based on the user's message.

Dependencies:
- uuid: For generating unique identifiers for conversations and messages.
- datetime: For handling date and time. 
"""

from ..models import Conversations, Message
import uuid
from datetime import datetime

def create_conversation_and_first_message(user, user_message):
    # Generate title with the first 5 words
    def generate_title(text, word_limit=5):
        words = text.strip().split()
        return ' '.join(words[:word_limit]) + ('...' if len(words) > word_limit else '')

    # Create new conversation with dynamic title
    conversation = Conversations.create(
        id_conversation=uuid.uuid4(),
        user_id=user.pk,
        title=generate_title(user_message),
        message_ids=[],
        created_at=datetime.utcnow()
    )
    
    # Create first message
    first_message = Message.create(
        id_message=uuid.uuid4(),
        id_conversation=conversation.id_conversation,
        sender='user',
        content=user_message,
        created_at=datetime.utcnow()
    )

    # Associate conversation ID at first message (if necessary)
    first_message.id_conversation = conversation.id_conversation
    first_message.save()

    return conversation, first_message