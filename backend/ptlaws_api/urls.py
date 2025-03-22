from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import ChatView


urlpatterns = [
    path("chat/", ChatView.as_view(), name="chat"),
]
