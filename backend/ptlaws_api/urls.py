from django.urls import path
from .views import ArticleView, ConversationView

urlpatterns = [
    path('articles/<uuid:id_article>/', ArticleView.as_view(), name="article-detail"),
    path('conversations/', ConversationView.as_view(), name='conversation-create')
]