from django.test import TestCase, Client
from accounts.models import CustomUser
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class IntegrationTestCase(APITestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            email='pavan@gmail.com',
            password='1234'
        )

    def test_admin_accessible(self):
        """Test that admin interface is accessible"""
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)  # Redirect to login


class DatabaseTestCase(TestCase):
    def test_user_creation(self):
        """Test user model works correctly"""
        user = CustomUser.objects.create_user(
            username='Raju',
            email='raju@gmail.com',
            password='1234'
        )
        self.assertEqual(user.username, 'Raju')
        self.assertEqual(user.email, 'raju@gmail.com')
        self.assertTrue(user.check_password('1234'))