from ..models import Conversations, Message
from uuid import uuid4
from datetime import datetime

def create_conversation_and_first_message(user, message_text):
    # 1. Create a new conversation
    conversation = Conversations.create(
        id_conversation=uuid4(),
        user_id=user.user_id,
        title=message_text[:40],  # A simple title based on the 1st message
        created_at=datetime.utcnow(),
        message_ids=[]
    )

    # 2. Create the first user message
    message = Message.create(
        id_message=uuid4(),
        id_conversation=conversation.id_conversation,
        sender="user",
        content=message_text,
        created_at=datetime.utcnow()
    )

    # 3. Add the message to the list
    conversation.message_ids.append(message.id_message)
    conversation.save()

    return conversation, message