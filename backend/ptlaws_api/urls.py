from django.urls import path
from .views import ArticleView, CreateConversationView, GetConversationView

urlpatterns = [
    path('articles/<uuid:id_article>/', ArticleView.as_view(), name="article-detail"),
    path('conversations/', CreateConversationView.as_view(), name='conversation-create'),
    path('conversations/<uuid:user_id>', GetConversationView.as_view(), name='get-conversations')
]