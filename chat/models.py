from django.db import models
from django.contrib.auth.models import User
    
class Conversations(models.Model):
    participants = models.ManyToManyField(User, related_name="participants", unique=False)

class Messages(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender", unique=False)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver", unique=False)
    conversation = models.ForeignKey(Conversations, related_name="conversations")
    message_content = models.TextField(max_length=500, default='', blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False, blank=False)
    
class Winks(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winks_sender", unique=False)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winks_receiver", unique=False)
    created_on = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False, blank=False)

class Views(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="views_sender", unique=False)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="views_receiver", unique=False)
    created_on = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False, blank=False)  

class Reject(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rejected_sender", unique=False)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rejected_receiver", unique=False)
    created_on = models.DateTimeField(auto_now_add=True)
