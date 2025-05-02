"""
tests.py

This file contains the test cases for the user authentication system.

It includes tests for user registration, login, token refresh, and access to protected routes.
The tests use Django's TestCase and DRF's APIClient to simulate requests and check responses.
The tests ensure that the authentication system works as expected and that users can register, log in, and access protected resources.
The tests also check that the correct status codes and response data are returned for each operation.
The test cases are organized into a single class, UserAuthTests, which contains methods for each test case.

Tests:
- test_register_user: Tests user registration.
- test_login_user: Tests user login.
- test_access_protected_route: Tests access to a protected route after login.
- test_refresh_token: Tests token refresh functionality.

This file is part of the Django REST Framework authentication system.
It is designed to work with the Django framework and the Django REST Framework (DRF).
It is important to ensure that the authentication system is secure and functions correctly.
"""

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status


class UserAuthTests(TestCase):
    def setUp(self):
        self.client_api = APIClient()
        self.register_url = "/api/users/register/"
        self.login_url = "/api/users/login/"
        self.token_refresh_url = "/api/users/token/refresh/"
        self.protected_url = "/api/users/protected/"

        self.user_data = {
            "email": "test@example.com",
            "username": "TestUser",
            "password": "testpass123",
            "password2": "testpass123"
        }

    def test_register_user(self):
        response = self.client_api.post(self.register_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("user", response.data)

    def test_login_user(self):
        self.client_api.post(self.register_url, self.user_data, format='json')
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
        self.test_login_user()
        self.client_api.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        response = self.client_api.get(self.protected_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_refresh_token(self):
        self.test_login_user()
        response = self.client_api.post(self.token_refresh_url, {
            "refresh": self.refresh_token
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)