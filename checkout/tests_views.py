from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
from django.http import HttpResponsePermanentRedirect
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Subscription
import stripe
from dating_app import settings

class TestViews(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='foo',
                                 email='foo@test.com',
                                 password='bar')
        
        test_user_two = User.objects.create_user(username='foo3',
                                 email='foo3@test.com',
                                 password='bar')

    # Test post to subscribe page subscribes user (no previous subscription)
    def test_post_subscribe_page_no_previous_sub(self):
        
        token = stripe.Token.create(
            card={
                "number": '4242424242424242',
                "exp_month": 1,
                "exp_year": 2035,
                "cvc": '123'
            },
        )
        
        user = self.client.login(username='foo3', password='bar')
        current_user = User.objects.get(username='foo3')
        
        page = self.client.post(reverse('subscribe'), 
                                { 'full_name':'foo bar',
                                  'phone_number':'0123456789',
                                  'country':'foo',
                                  'postcode':'foo',
                                  'town_or_city':'foo',
                                  'street_address1':'foo',
                                  'street_address2':'foo',
                                  'county':'foo',
                                  'stripe_id': token.id,
                                  'credit_card_number':4242424242424242,
                                  'cvv':123,
                                  'expiry_month':1,
                                  'expiry_year':2035,
                                  'plans': 'plan_F5eyGdYCvZPtON'} )
        
        self.assertRedirects(page, reverse('index'), status_code=302)
        
        # Check subscription created for customer in Stripe
        subscription = Subscription.objects.get(user_id=current_user.id)
        customer = stripe.Customer.retrieve(subscription.customer_id)
        self.assertEqual(1, customer.subscriptions.total_count)
        
        # Delete subscription for subsequent tests
        stripe.Customer.delete(subscription.customer_id)
        
    # Test post to subscribe page subscribes user (previous subscription)
    def test_post_subscribe_page_previous_sub(self):
        # Create Stripe token
        token = stripe.Token.create(
            card={
                "number": '4242424242424242',
                "exp_month": 1,
                "exp_year": 2035,
                "cvc": '123'
            },
        )
        
        user = self.client.login(username='foo3', password='bar')
        current_user = User.objects.get(username='foo3')
        # Create customer in Stripe
        customer = stripe.Customer.create(
                card = token.id,
                description = current_user.email,
                email = current_user.email
            )
        # Create subscription
        subscription = Subscription(plan="monthly", customer_id=customer.id, user_id=current_user.id)
        subscription.save()
        
        # Create Stripe token
        token = stripe.Token.create(
            card={
                "number": '4242424242424242',
                "exp_month": 1,
                "exp_year": 2035,
                "cvc": '123'
            },
        )
        page = self.client.post(reverse('subscribe'), 
                                { 'full_name':'foo bar',
                                  'phone_number':'0123456789',
                                  'country':'foo',
                                  'postcode':'foo',
                                  'town_or_city':'foo',
                                  'street_address1':'foo',
                                  'street_address2':'foo',
                                  'county':'foo',
                                  'stripe_id': token.id,
                                  'credit_card_number':4242424242424242,
                                  'cvv':123,
                                  'expiry_month':1,
                                  'expiry_year':2035,
                                  'plans': 'plan_F5eyGdYCvZPtON'} )
        
        self.assertRedirects(page, reverse('index'), status_code=302)
        
        # Check subscription created for customer in Stripe
        customer = stripe.Customer.retrieve(customer.id)
        self.assertEqual(1, customer.subscriptions.total_count)
        
        # Delete customer for subsequent tests
        stripe.Customer.delete(subscription.customer_id)
        