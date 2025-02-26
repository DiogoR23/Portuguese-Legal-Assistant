from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.ListUserView.as_view(), name='user-list'),
    path('create-user/', views.CreateUSerView.as_view(), name='user-create'),
    path('ai-response/', views.AIResponseView.as_view(), name='ai-response')
]