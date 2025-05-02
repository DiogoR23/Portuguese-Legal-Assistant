"""
urls.py

This file contains the URL patterns for the user authentication app.
It includes paths for user registration, login, token refresh, and a protected view.
- `register/`: Endpoint for user registration.
- `login/`: Endpoint for user login.
- `token/refresh/`: Endpoint for refreshing JWT tokens.
- `protected/`: A protected view that requires authentication.

Each view is associated with a specific class-based view from the `views.py` file.
The `TokenRefreshView` is imported from `rest_framework_simplejwt.views` to handle token refresh functionality.
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import RegisterView, LoginView, ProtectedView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('protected/', ProtectedView.as_view(), name='user-protected')
]