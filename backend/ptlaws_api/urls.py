"""
urls.py

This module defines the URL patterns for the chat application.
It includes paths for various views related to chat functionality, such as listing conversations, creating conversations, deleting conversations, updating conversation titles, and listing messages within a conversation.

Each URL pattern is associated with a specific view class that handles the request.
The URL patterns are defined using Django's path function, which maps a URL to a view.
The URL patterns are as follows:
- `chat/`: Maps to the `ChatView` class, which handles chat-related functionality.
- `conversations/`: Maps to the `ListUserConversationsView` class, which lists all conversations for the authenticated user.
- `conversations/<uuid:conversation_id>/messages/`: Maps to the `ListConversationsMessagesView` class, which lists messages for a specific conversation.
- `create/conversations/`: Maps to the `CreateConversationView` class, which creates a new conversation.
- `conversations/<uuid:conversation_id>/`: Maps to the `DeleteConversationView` class, which deletes a specific conversation.
- `conversations/<uuid:conversation_id>/title/`: Maps to the `UpdateConversationTitleView` class, which updates the title of a specific conversation.

This module is part of the ptlaws_api application and is responsible for routing requests to the appropriate views based on the URL patterns defined.
"""

from django.urls import path

from .views import ChatView, ListConversationsMessagesView, ListUserConversationsView, CreateConversationView, DeleteConversationView, UpdateConversationTitleView


urlpatterns = [
    path("chat/", ChatView.as_view(), name="chat"),
    path("conversations/", ListUserConversationsView.as_view(), name="list-conversations"),
    path("conversations/<uuid:conversation_id>/messages/", ListConversationsMessagesView.as_view(), name="conversation-messages"),
    path("create/conversations/", CreateConversationView.as_view(), name="create-conversation"),
    path("conversations/<uuid:conversation_id>/", DeleteConversationView.as_view(), name="delete-conversation"),
    path("conversations/<uuid:conversation_id>/title/", UpdateConversationTitleView.as_view(), name="update-conversation-title"),
]
