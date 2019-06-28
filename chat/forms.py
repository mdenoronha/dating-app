from .models import Messages, Conversations
from django import forms
from django.forms import Textarea

class MessageForm(forms.ModelForm):

    class Meta:
        model = Messages
        fields = ('message_content', )

# class SmallMessageForm(forms.ModelForm):

#     class Meta:
#         model = Messages
#         fields = ('message_content', )        
#         widgets = {
#           'message_content': Textarea(attrs={'rows':3, 'cols':50}),}