from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
from profiles.models import Profile
from checkout.models import Subscription
import stripe

# Create your tests here.
class TestViews(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='foo',
                                 email='foo@test.com',
                                 password='bar')
        
        test_user_two = User.objects.create_user(username='foo3',
                                 email='foo3@test.com',
                                 password='bar')
    
    # Test get account page returns 200 response
    def test_get_account_page(self):
        self.client.login(username='foo', password='bar')
        page = self.client.get(reverse('account'))
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, 'account.html')
     
    # Test post to account page with user form  
    def test_post_account_page_user_form(self):
        self.client.login(username='foo', password='bar')
        current_user = User.objects.get(username='foo')
        # User's email is unchanged
        self.assertEqual(current_user.email, 'foo@test.com')
        
        page = self.client.post(reverse('account'), 
                                        { 'email': 'bar@test.com',
                                          'username': 'foo',
                                          'confirm_password': 'bar',
                                          'account-change-submit': 'account-change-submit' } )
        # User's email has changed
        current_user = User.objects.get(username='foo')
        self.assertNotEqual(current_user.email, 'foo@test.com')
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, 'account.html')
        
    # Test post to account page with password form  
    def test_post_account_page_password_form(self):
        self.client.login(username='foo', password='bar')
        current_user = User.objects.get(username='foo')
        user = auth.get_user(self.client)

        # # User's can log in with original password
        self.assertTrue(current_user.is_authenticated())
        page = self.client.post(reverse('account'), 
                                        { 'old_password': 'bar',
                                          'new_password1': 'foobarbar',
                                          'new_password2': 'foobarbar',
                                          'password-change-submit': 'password-change-submit' } )
                                          
        # # User cannot log in with original password
        request = page.wsgi_request
        logout(request)
        self.client.login(username='foo', password='bar')
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated())
        
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, 'account.html')
        
    # Test cancel page cancels subscription and redirects to account 
    def test_get_cancel_sub(self):
        self.client.login(username='foo', password='bar')
        current_profile = Profile.objects.get(user_id__username='foo')
        
        # Set premium status
        current_profile.is_premium = True
        current_profile.save()
        subscription = Subscription(plan="monthly", customer_id="cus_FMdSeBRaEVZlmh", user_id=current_profile.user.id)
        subscription.save()
        sub_id = 'sub_FMdVFN7OCb4D3O'
        
        # Test subscription is currently active
        active_subscription = stripe.Subscription.retrieve(sub_id)
        self.assertEqual(active_subscription.cancel_at_period_end, False)
        
        page = self.client.get('/my-account/cancel/%s' % sub_id)
        self.assertRedirects(page, reverse('account'), status_code=302)
        
        active_subscription = stripe.Subscription.retrieve(sub_id)
        self.assertNotEqual(active_subscription.cancel_at_period_end, False)
        
        # Resubscribe for subsequent tests
        stripe.Subscription.modify(
            sub_id,
            cancel_at_period_end=False
        )

    # Test reactivate page reactivates subscription and redirects to account 
    def test_get_reactivate_sub(self):
        self.client.login(username='foo', password='bar')
        current_profile = Profile.objects.get(user_id__username='foo')
        
        # Set premium status
        current_profile.is_premium = True
        current_profile.save()
        subscription = Subscription(plan="monthly", customer_id="cus_FMdSeBRaEVZlmh", user_id=current_profile.user.id)
        subscription.save()
        sub_id = 'sub_FMdVFN7OCb4D3O'
        
        # Cancel subscription
        stripe.Subscription.modify(
            sub_id,
            cancel_at_period_end=True
        )
        
        
        page = self.client.get('/my-account/reactivate/%s' % sub_id)
        self.assertRedirects(page, reverse('account'), status_code=302)
        
        active_subscription = stripe.Subscription.retrieve(sub_id)
        self.assertEqual(active_subscription.cancel_at_period_end, False)
        
        # Resubscribe for subsequent tests in case of any errors
        stripe.Subscription.modify(
            sub_id,
            cancel_at_period_end=False
        )
    
   