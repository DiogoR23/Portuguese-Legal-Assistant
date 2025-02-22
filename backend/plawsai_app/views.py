from django.shortcuts import render
from .models import Conversation, QuestionAnswerHistory

# Create your views here.
def conversation_history(request, id_conversation):
    conversation = Conversation.objects.get(id=id_conversation)
    q_a = QuestionAnswerHistory.objects.filter(conversation = conversation)

    return render(request, "conversation_history.html", {"questions_answers": q_a})

