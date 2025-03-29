from django.urls import path

from .views import ChatView, ListConversationsMessagesView, ListUserConversationsView, CreateConversationView


urlpatterns = [
    path("chat/", ChatView.as_view(), name="chat"),
    path("conversations/", ListUserConversationsView.as_view(), name="list-conversations"),
    path("conversations/<uuid:conversation_id>/messages/", ListConversationsMessagesView.as_view(), name="conversation-messages"),
    path("create/conversations/", CreateConversationView.as_view(), name="create-conversation")
]
