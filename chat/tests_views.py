from django.test import TestCase
from django.contrib.auth.models import User
from .models import Conversations, Messages, Winks, Reject
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib import auth
# from django.http import HttpResponsePermanentRedirect
# from django.core.files.uploadedfile import SimpleUploadedFile
from checkout.models import Subscription
from profiles.models import Profile
from django.utils import six
import json

# Create your tests here.
class TestViews(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='foo',
                                 email='foo@test.com',
                                 password='bar')
        
        test_user_two = User.objects.create_user(username='foo3',
                                 email='foo3@test.com',
                                 password='bar')
                                 
        """
        A customer in Stripe under id 'cus_FMdSeBRaEVZlmh' is used
        """
        
    # Test get chat page
    def test_chat_page(self):
        self.client.login(username='foo', password='bar')
        current_profile = Profile.objects.get(user_id__username='foo')
        receiver_profile = User.objects.get(username='foo3')
        # Make user premium
        current_profile.is_premium = True
        current_profile.save()
        subscription = Subscription(plan="monthly", customer_id="cus_FMdSeBRaEVZlmh", user_id=current_profile.user.id)
        subscription.save()
        # Make conversation
        conversation = Conversations()
        conversation.save()
        conversation.participants.add(current_profile.user.id)
        conversation.participants.add(receiver_profile.id)

        page = self.client.get('/chat/%s' % conversation.id)
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, 'chat.html')
    
    # Test post chat page creates message and redirects back to chat
    def test_post_chat_page(self):
        self.client.login(username='foo', password='bar')
        current_profile = Profile.objects.get(user_id__username='foo')
        receiver_profile = User.objects.get(username='foo3')
        # Make user premium
        current_profile.is_premium = True
        current_profile.save()
        subscription = Subscription(plan="monthly", customer_id="cus_FMdSeBRaEVZlmh", user_id=current_profile.user.id)
        subscription.save()
        # Make conversation
        conversation = Conversations()
        conversation.save()
        conversation.participants.add(current_profile.user.id)
        conversation.participants.add(receiver_profile.id)
        
        page = self.client.post(reverse('chat', kwargs={'id':conversation.id}), {
                                        'message_content': 'foo'})
        
        self.assertTrue(Messages.objects.get(message_content='foo'))
        self.assertRedirects(page, '/chat/%s' % conversation.id, status_code=302)

    # Test get chat home page (no previous conversations)
    def test_get_chat_home_no_previous_conversations(self):
        self.client.login(username='foo', password='bar')
        current_profile = Profile.objects.get(user_id__username='foo')
        # Make user premium
        current_profile.is_premium = True
        current_profile.save()
        subscription = Subscription(plan="monthly", customer_id="cus_FMdSeBRaEVZlmh", user_id=current_profile.user.id)
        subscription.save()
        page = self.client.get('/chat/home/')
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, 'chat_home.html')
        
    # Test get chat home page (previous conversations) (received message)
    def test_get_chat_home_previous_conversations_received_message(self):
        self.client.login(username='foo', password='bar')
        current_profile = Profile.objects.get(user_id__username='foo')
        receiver_profile = Profile.objects.get(user_id__username='foo3')
        # Make user premium
        current_profile.is_premium = True
        current_profile.save()
        subscription = Subscription(plan="monthly", customer_id="cus_FMdSeBRaEVZlmh", user_id=current_profile.user.id)
        subscription.save()
        
        # Create conversation and messages
        conversation = Conversations()
        conversation.save()
        conversation.participants.add(current_profile.user.id)
        conversation.participants.add(receiver_profile.user.id)
        message = Messages(message_content="foo", is_read=False, receiver_id=current_profile.user.id, sender_id=receiver_profile.user.id, conversation_id=conversation.id)
        message.save()
        
        page = self.client.get('/chat/home/')
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, 'chat_home.html')
        
    # Test get chat home page (previous conversations) (sent message)
    def test_get_chat_home_previous_conversations_sent_message(self):
        self.client.login(username='foo', password='bar')
        current_profile = Profile.objects.get(user_id__username='foo')
        receiver_profile = Profile.objects.get(user_id__username='foo3')
        # Make user premium
        current_profile.is_premium = True
        current_profile.save()
        subscription = Subscription(plan="monthly", customer_id="cus_FMdSeBRaEVZlmh", user_id=current_profile.user.id)
        subscription.save()
        
        # Create conversation and messages
        conversation = Conversations()
        conversation.save()
        conversation.participants.add(current_profile.user.id)
        conversation.participants.add(receiver_profile.user.id)
        message = Messages(message_content="foo", is_read=False, receiver_id=receiver_profile.user.id, sender_id=current_profile.user.id, conversation_id=conversation.id)
        message.save()
        
        page = self.client.get('/chat/home/')
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, 'chat_home.html')
    
    # Test get winks page
    def test_get_winks(self):
        self.client.login(username='foo', password='bar')
        page = self.client.get('/chat/winks/')
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, 'winks.html')
        
    # Test get views page
    def test_get_views(self):
        self.client.login(username='foo', password='bar')
        current_profile = Profile.objects.get(user_id__username='foo')
        # Make user premium
        current_profile.is_premium = True
        current_profile.save()
        subscription = Subscription(plan="monthly", customer_id="cus_FMdSeBRaEVZlmh", user_id=current_profile.user.id)
        subscription.save()
        page = self.client.get('/chat/views/')
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, 'views.html')
   
    # Test message check returns JSON data 
    def test_ajax_new_message_check(self):
        self.client.login(username='foo', password='bar')
        current_profile = Profile.objects.get(user_id__username='foo')
        receiver_profile = User.objects.get(username='foo3')
        # Create conversation and messages
        conversation = Conversations()
        conversation.save()
        conversation.participants.add(current_profile.user.id)
        conversation.participants.add(receiver_profile.id)
        message = Messages(message_content="foo", is_read=False, receiver_id=current_profile.id, sender_id=receiver_profile.id, conversation_id=conversation.id)
        message.save()
        # Make user premium
        current_profile.is_premium = True
        current_profile.save()
        subscription = Subscription(plan="monthly", customer_id="cus_FMdSeBRaEVZlmh", user_id=current_profile.user.id)
        subscription.save()
        
        
        page = self.client.get(reverse('new_message_check'), {
                                        'url_id': conversation.id}, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
                                        
        response_content = page.content
        # https://stackoverflow.com/questions/27472663/how-to-use-djangos-assertjsonequal-to-verify-response-of-view-returning-jsonres
        if six.PY3:
            response_content = str(response_content, encoding='utf8')

        self.assertJSONEqual(
            response_content,
            {'conversation' : True}
        )
    
    # Test wink returns correct JSON - last wink unread
    def test_ajax_wink_not_read(self):
        self.client.login(username='foo', password='bar')
        current_user = User.objects.get(username='foo')
        receiver_user = User.objects.get(username='foo3')
        # Create unread wink
        wink = Winks(receiver=receiver_user, sender=current_user) 
        wink.save()
        page = self.client.get(reverse('wink'), {
                                        'receiver_id': receiver_user.id}, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        
        response_content = page.content
        if six.PY3:
            response_content = str(response_content, encoding='utf8')

        self.assertJSONEqual(
            response_content,
            {'message' : "Member hasn't viewed your last wink yet"}
        )
        
    # Test wink returns correct JSON - no unread winks
    def test_ajax_wink_no_unread(self):
        self.client.login(username='foo', password='bar')
        receiver_profile = User.objects.get(username='foo3')
        page = self.client.get(reverse('wink'), {
                                        'receiver_id': receiver_profile.id}, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        
        response_content = page.content
        if six.PY3:
            response_content = str(response_content, encoding='utf8')

        self.assertJSONEqual(
            response_content,
            {'message' : 'Wink successfully sent.'}
        )
        
    # Test reject creates reject record (as one is not yet created) and returns 204 response
    def test_ajax_reject(self):
        self.client.login(username='foo', password='bar')
        receiver_user = User.objects.get(username='foo3')
        current_user = User.objects.get(username='foo')
        
        # Record not yet created
        reject_record = Reject.objects.filter(sender_id=current_user, receiver_id=receiver_user).exists()
        self.assertFalse(reject_record)
    
        page = self.client.get(reverse('reject'), {
                                        'receiver_id': receiver_user.id}, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        
        response_content = page.content
        if six.PY3:
            response_content = str(response_content, encoding='utf8')
        
        self.assertJSONEqual(
            response_content,
            {'message' : 'Member successfully skipped'}
        )
        
    # Test chat ajax returns JSON and creates conversation and message (conversation not yet exists)
    def test_ajax_message_no_conversation(self):
        self.client.login(username='foo', password='bar')
        receiver_user = User.objects.get(username='foo3')
        current_user = User.objects.get(username='foo')
        # Make user premium
        current_user.profile.is_premium = True
        current_user.profile.save()
        subscription = Subscription(plan="monthly", customer_id="cus_FMdSeBRaEVZlmh", user_id=current_user.id)
        subscription.save()
        
        page = self.client.post(reverse('new_message'), {
                                        'message_receiver': receiver_user.id, 'message_content': 'foo'}, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        
        response_content = page.content
        if six.PY3:
            response_content = str(response_content, encoding='utf8')
        
        message = Messages.objects.filter(message_content='foo', sender_id=current_user, receiver_id=receiver_user).exists()
        self.assertTrue(message)
        self.assertJSONEqual(
            response_content,
            {'message' : 'Message Successfully Sent'}
        )
        
    # Test chat ajax returns JSON and creates message (conversation already exists)
    def test_ajax_message_conversation_exists(self):
        self.client.login(username='foo', password='bar')
        receiver_user = User.objects.get(username='foo3')
        current_user = User.objects.get(username='foo')
        # Make user premium
        current_user.profile.is_premium = True
        current_user.profile.save()
        subscription = Subscription(plan="monthly", customer_id="cus_FMdSeBRaEVZlmh", user_id=current_user.id)
        subscription.save()
        
        # Create conversation
        conversation = Conversations()
        conversation.save()
        conversation.participants.add(current_user.id)
        conversation.participants.add(receiver_user.id)
        conversation.save()
        
        page = self.client.post(reverse('new_message'), {
                                        'message_receiver': receiver_user.id, 'message_content': 'foo'}, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        
        
        response_content = page.content
        if six.PY3:
            response_content = str(response_content, encoding='utf8')
        
        message = Messages.objects.filter(message_content='foo', sender_id=current_user, receiver_id=receiver_user).exists()
        self.assertTrue(message)
        self.assertJSONEqual(
            response_content,
            {'message' : 'Message Successfully Sent'}
        )
        
    # Test AJAX request reads all messages in conversation
    def test_ajax_read_messages(self):
        self.client.login(username='foo', password='bar')
        receiver_user = User.objects.get(username='foo3')
        current_user = User.objects.get(username='foo')
        
        # Create conversation and messages
        conversation = Conversations()
        conversation.save()
        conversation.participants.add(current_user.id)
        conversation.participants.add(receiver_user.id)
        message = Messages(message_content="foo", is_read=False, receiver_id=current_user.id, sender_id=receiver_user.id, conversation_id=conversation.id)
        message.save()

        page = self.client.get(reverse('read_messages'), {
                                        'url_id': 1}, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
                                        
        response_content = page.content
        if six.PY3:
            response_content = str(response_content, encoding='utf8')
        
        message = Messages.objects.get(pk=message.id)
        
        self.assertEqual(message.is_read, True)
        self.assertJSONEqual(
            response_content,
            {'conversation' : False}
        )
        
    # Test ajax read wink returns 204 status code
    def test_ajax_read_wink(self):
        self.client.login(username='foo', password='bar')
        page = self.client.post(reverse('read_wink'), {
                                        'page': 1}, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        
        self.assertEqual(page.status_code, 204)
    
    # Test ajax read view returns redirect directive (not premium)   
    def test_ajax_read_view_not_premium(self):
        self.client.login(username='foo', password='bar')
        page = self.client.post(reverse('read_view'), {
                                        'page': 1}, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        
        response_content = page.content
        if six.PY3:
            response_content = str(response_content, encoding='utf8')
        
        self.assertJSONEqual(
            response_content,
            {'redirect' : '/subscribe'}
        )
        
    # Test ajax read view returns 204 response (user premium)   
    def test_ajax_read_view_premium(self):
        self.client.login(username='foo', password='bar')
        current_user = User.objects.get(username='foo')
        # Make user premium
        current_user.profile.is_premium = True
        current_user.profile.save()
        subscription = Subscription(plan="monthly", customer_id="cus_FMdSeBRaEVZlmh", user_id=current_user.id)
        subscription.save()
        
        page = self.client.post(reverse('read_view'), {
                                        'page': 1}, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        
        self.assertEqual(page.status_code, 204)

   