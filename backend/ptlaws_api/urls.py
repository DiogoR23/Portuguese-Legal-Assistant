from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.ListUserView.as_view(), name='user-list'),
    path('create-user/', views.CreateUserView.as_view(), name='user-create'),
    path('ptlawsai/', views.AIResponseView.as_view(), name='ptlaws-ai')
]