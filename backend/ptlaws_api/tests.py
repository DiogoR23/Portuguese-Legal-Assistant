from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
import uuid

# Create your tests here.
class UserAuthTests(TestCase):
    def setUp(self):
        """Initial Test Configuration."""
        self.client_api = APIClient()
        self.register_url = "/api/register/"
        self.login_url = "/api/login/"
        self.token_refresh_url = "/api/token/refresh/"
        self.protected_url = "/api/protected/"

        self.user_data = {
            "email": "test@example.com",
            "username": "TestUser",
            "password": "testpass123"
        }


    def test_register_user(self):
        """Test to check if a user can register."""
        response = self.client_api.post(self.register_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("user", response.data)


    def test_login_user(self):
        """Login test and obtain JWT."""
        # First, register a user
        self.client_api.post(self.register_url, self.user_data, format='json')

        # Now, try to Login
        response = self.client_api.post(self.login_url, {
            "email": self.user_data['email'],
            "password": self.user_data['password']
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)
        self.assertIn("refresh_token", response.data)

        self.access_token = response.data['access_token']
        self.refresh_token = response.data['refresh_token']


    def test_access_protected_route(self):
        """Test to verify if a protected route demand authentication."""
        self.test_login_user()
        self.client_api.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        response = self.client_api.get(self.protected_url) # Try to access a protected route
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_refresh_token(self):
        """Test to verify if the refresh token works."""
        # Login to get the RefreshToken
        self.test_login_user()

        response = self.client_api.post(self.token_refresh_url, {
            "refresh": self.refresh_token
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)