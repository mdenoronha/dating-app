from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth

class TestViews(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='foo',
                                 email='foo@test.com',
                                 password='bar')
        
        test_user_two = User.objects.create_user(username='foo3',
                                 email='foo3@test.com',
                                 password='bar')
    
    # Test get search page returns 200 response
    def test_get_search_page(self):
        self.client.login(username='foo', password='bar')
        page = self.client.get(reverse('search'))
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, 'search.html')
   