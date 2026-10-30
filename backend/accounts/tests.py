from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class AccountsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_registration(self):
        response = self.client.post(reverse('accounts:register'), {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'Person',
            'email': 'new@example.com',
            'phone': '1234567890',
            'password': 'safePassword123',
            'confirm_password': 'safePassword123'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertTrue(hasattr(User.objects.get(username='newuser'), 'profile'))

    def test_login_and_logout(self):
        User.objects.create_user(username='loginuser', password='password123', email='log@test.com')
        
        # Test login
        response = self.client.post(reverse('accounts:login'), {
            'username': 'loginuser',
            'password': 'password123'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome back')

        # Test logout
        response = self.client.get(reverse('accounts:logout'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You have been logged out')
