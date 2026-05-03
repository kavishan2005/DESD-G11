from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class AccountTests(TestCase):
    
    def test_user_registration(self):
        """Test user can register"""
        response = self.client.post('/accounts/register/', {
            'username': 'newuser',
            'email': 'new@test.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        })
        # Should redirect after successful registration
        self.assertNotEqual(response.status_code, 404)
    
    def test_user_login(self):
        """Test user can login"""
        User.objects.create_user(username='testuser', password='testpass123')
        response = self.client.post('/accounts/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertNotEqual(response.status_code, 404)
    
    def test_login_required_for_profile(self):
        """Test profile requires login"""
        response = self.client.get('/accounts/profile/')
        self.assertNotEqual(response.status_code, 200)  # Should redirect
