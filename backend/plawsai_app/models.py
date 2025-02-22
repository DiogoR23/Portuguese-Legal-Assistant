from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation by {self.user.username} - Started in {self.start}"


class QuestionAnswerHistory(models.Model):
    conversation = models.ForeignKey(Conversation, related_name="questions_answers", on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Question: {self.question} ... - Answer: {self.answer}"