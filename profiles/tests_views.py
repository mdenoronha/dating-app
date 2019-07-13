from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile
from .views import logout
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
from django.http import HttpResponsePermanentRedirect
from django.core.files.uploadedfile import SimpleUploadedFile
from checkout.models import Subscription

class TestViews(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='foo',
                                 email='foo@test.com',
                                 password='bar')
        
        test_user_two = User.objects.create_user(username='foo3',
                                 email='foo3@test.com',
                                 password='bar')
        
    # Test login page, user not authenticated
    def test_login_page_user_not_authenticated(self):
        page = self.client.get('/accounts/login/')
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, 'login.html')
    
    # Test login page redirects to home, user is authenticated
    def test_login_page_user_authenticated(self):
        self.client.login(username='foo', password='bar')
        page = self.client.get('/accounts/login/')
        self.assertRedirects(page, '/home/', status_code=302)
        
    # Test logout page redirects to preregister
    def test_logout_page(self):
        self.client.login(username='foo', password='bar')
        page = self.client.get('/accounts/logout/')
        self.assertRedirects(page, '/', status_code=302)
        
    # Test delete redirects to preregister
    def test_delete_page(self):
        self.client.login(username='foo', password='bar')
        page = self.client.get('/accounts/delete/')
        self.assertRedirects(page, '/', status_code=302)
        
    # Test get register page
    def test_get_register_page(self):
        page = self.client.get('/accounts/register/')
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, 'register.html')

    # Test post register page
    def test_post_register_page(self):
        page = self.client.post(reverse('register'), 
                                { 'username':'foo2',
                                  'email':'foo@test.com',
                                  'password1':'bar123456',
                                  'password2':'bar123456' } )
        self.assertRedirects(page, reverse('create_profile'), status_code=302)
    
    # Test get create profile page
    def test_get_create_profile_page(self):
        self.client.login(username='foo', password='bar')
        page = self.client.get('/accounts/create-profile/')
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, 'create-profile.html')

    # Test post create profile page
    def test_post_create_profile_page(self):
        user = self.client.login(username='foo', password='bar')
        # Sample image for profile photo form
        image = SimpleUploadedFile(name='foo.gif', 
                   content=b'GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00')

        page = self.client.post(reverse('create_profile'), 
                                        { 'user': user,
                                          'bio':'foo',
                                          'gender':'MALE',
                                          'hair_length':'LONG',
                                          'ethnicity': 'WHITE',
                                          'relationship_status': 'DIVORCED',
                                          'education': 'COLLEGE',
                                          'height': '180.34',
                                          'hair_colour': 'BROWN',
                                          'body_type': 'AVERAGE',
                                          'looking_for': 'MALE',
                                          'children': True,
                                          'location': 'Foo',
                                          'citylat': 10.10,
                                          'citylong': 10.10,
                                          'birth_date': '01/01/1990',
                                          'image': image,
                                          'form-TOTAL_FORMS': 1, 
                                           'form-INITIAL_FORMS': 0 
                                        } )
        
        profile = Profile.objects.get(bio='foo')
        self.assertTrue(profile)
        self.assertRedirects(page, '/accounts/verification-message/', status_code=302)
    
    # Test login functionality
    def test_login_authentication(self):
                                 
        response = self.client.post(reverse('login'), 
                                { 'username':'foo', 
                                  'password':'bar' } )
        
        logged_in_user = auth.get_user(self.client)
        self.assertTrue(logged_in_user.is_authenticated())
        
    # Test get member page
    def test_get_member_page(self):
        self.client.login(username='foo', password='bar')
        user = User.objects.first()
        page = self.client.get('/accounts/member/%s' % user.id )
        
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, 'member.html')
    
    # Test post member page redirects to subscribe (for non premium user)  
    def test_post_member_page(self):
        visited_user = User.objects.get(username='foo3')
        current_user = User.objects.get(username='foo')
        
        
        # Sexuality and gender options set to allow visit
        current_profile = Profile.objects.get(user_id=current_user.id)
        current_profile.looking_for = "MALE"
        current_profile.gender = "FEMALE"
        current_profile.save()
        visited_profile = Profile.objects.get(user_id=visited_user.id)
        visited_profile.looking_for = "FEMALE"
        visited_profile.gender = "MALE"
        visited_profile.save()
        
        self.client.login(username='foo', password='bar')
        page = self.client.post('/accounts/member/%s' % visited_user.id, 
                                { 'message_content':'foo',
                                  'message_submit': 'message_submit'} )
                                
        self.assertRedirects(page, '/subscribe/', status_code=302)
    
    # Test post member page redirects to chat page (premium user)  
    def test_post_member_page_premium_user(self):
        visited_user = User.objects.get(username='foo3')
        current_user = User.objects.get(username='foo')
        
        
        # Sexuality and gender options set to allow visit
        current_profile = Profile.objects.get(user_id=current_user.id)
        current_profile.looking_for = "MALE"
        current_profile.gender = "FEMALE"
        # Set premium status
        current_profile.is_premium = True
        current_profile.save()
        subscription = Subscription(plan="monthly", customer_id="cus_FMdSeBRaEVZlmh", user_id=current_user.id)
        subscription.save()
        
        visited_profile = Profile.objects.get(user_id=visited_user.id)
        visited_profile.looking_for = "FEMALE"
        visited_profile.gender = "MALE"
        visited_profile.save()
        
        self.client.login(username='foo', password='bar')
        page = self.client.post('/accounts/member/%s' % visited_user.id, 
                                { 'message_content':'foo',
                                  'message_submit': 'message_submit'} )
                                
        self.assertRedirects(page, '/chat/1', status_code=302)
        
    # Test get member page redirects to index if gender and sexuality do not allow visit
    def test_get_member_page_non_match_sexuality(self):
        visited_user = User.objects.get(username='foo3')
        current_user = User.objects.get(username='foo')
        
        
        # Sexuality and gender options set to allow visit
        current_profile = Profile.objects.get(user_id=current_user.id)
        current_profile.looking_for = "FEMALE"
        current_profile.gender = "FEMALE"
        current_profile.save()
        visited_profile = Profile.objects.get(user_id=visited_user.id)
        visited_profile.looking_for = "FEMALE"
        visited_profile.gender = "MALE"
        visited_profile.save()
        
        self.client.login(username='foo', password='bar')
        page = self.client.get('/accounts/member/%s' % visited_user.id)
                                
        self.assertRedirects(page, '/home/', status_code=302)
    
    # Test logout functionality   
    def test_logout(self):
        self.client.login(username='foo', password='bar')
        page = self.client.get('/accounts/logout/')
        logged_in_user = auth.get_user(self.client)
        self.assertFalse(logged_in_user.is_authenticated())

    # Test verification page
    def test_verification_page(self):
        self.client.login(username='foo', password='bar')
        page = self.client.get('/accounts/verification-message/')
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, 'verification-message.html')