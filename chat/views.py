from django.shortcuts import render, reverse, redirect, render_to_response
from .forms import MessageForm
from .models import Conversations, Messages, Winks, Views, Reject
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib import messages
from profiles.views import looking_for_check
import time
from checkout.decorators import premium_required
from django.contrib.auth.decorators import login_required
import json as simplejson

"""
Checks if last message recieved by user is unread - used to check if a new message
has been recieved
"""
@login_required
@premium_required
def new_message_check(request):
    conversation_id = request.GET.get('url_id', None)
    is_read = Messages.objects.filter(conversation=conversation_id, receiver=request.user, is_read=False).exists()
    data = {
        'conversation': is_read
    }
    return JsonResponse(data)

"""
For AJAX function to set all messages in a conversation for a particular reciever
as read
"""
def read_messages(request):
    conversation_id = request.GET.get('url_id', None)
    messages = Messages.objects.filter(conversation=conversation_id)
    for message in messages:
        if message.receiver == request.user:
            message.is_read = True
            message.save()

    is_read = Messages.objects.filter(conversation=conversation_id, receiver=request.user, is_read=False).exists()
    data = {
        'conversation': is_read
    }
    return JsonResponse(data)

# Chat page, showing messages of a specific conversation
@login_required
@premium_required
def chat(request, id):
    page_ref = "chat"
    conversation_ids = Conversations.objects.filter(participants=request.user)
    
    all_conversations = {}
    is_read_check = {}
    for conversation in conversation_ids:  
        all_conversations[conversation.id] = Messages.objects.filter(conversation=conversation).last()

        # Is the last message recieved read? Used to update styling.
        last_message = Messages.objects.filter(conversation=conversation, receiver=request.user).last()
        if last_message:
            is_read_check[conversation.id] = last_message.is_read
        else: 
            is_read_check[conversation.id] = True
    
    messages = Messages.objects.filter(conversation=id)
    
    # Determine other conversation participant
    conversation = Conversations.objects.get(pk=id)
    participants = conversation.participants.all()
    for user in participants:
        if not user.id == request.user.id:
            receiver = user
    
    # If user has sent a message  
    if request.method == "POST":
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            # If user has tried sending a message to themselves
            if receiver.id == request.user.id:
                messages.success(request, "You can't send a message to yourself")
                return redirect(reverse('chat_home'))
                
            # Save submitted message
            message = message_form.save(commit=False)
            message.receiver = User.objects.get(id=receiver.id)
            message.sender = request.user
            message.conversation = conversation
            message.save()

        context = {
            'page_ref': page_ref,
            'user_messages': messages,
            'message_form':message_form,
            'all_conversations': all_conversations,
            'receiver': receiver,
            'conversation_id': int(id),
            'is_read_check': is_read_check
        }
        
        return redirect(reverse('chat', kwargs={'id':id}))
    else:
        message_form = MessageForm()
    
    context = {
        'page_ref': page_ref,
        'user_messages': messages,
        'message_form':message_form,
        'all_conversations': all_conversations,
        'receiver': receiver.id,
        'conversation_id': int(id),
        'is_read_check': is_read_check
    }
    
    return render(request, 'chat.html', context)
 
# Chat home page, which displays all conversations but no messages
@login_required  
@premium_required 
def chat_home(request):
    conversation_ids = Conversations.objects.filter(participants=request.user)

    all_conversations = {}
    is_read_check = {}
    for conversation in conversation_ids:  
        all_conversations[conversation.id] = Messages.objects.filter(conversation=conversation).last()
        
        # Is the last message recieved read? Used to update styling.
        last_message = Messages.objects.filter(conversation=conversation, receiver=request.user).last()
        if last_message:
            is_read_check[conversation.id] = last_message.is_read
        else: 
            is_read_check[conversation.id] = True

    context = {
        'user_messages': messages,
        'all_conversations': all_conversations,
        'conversation_id': None,
        'is_read_check': is_read_check
    }

    return render(request, 'chat_home.html', context)

# AJAX function to create wink record 
def wink(request):
    
    # Get id of user recipient
    receiver_id = request.GET.get('receiver_id')
    # If user tried to wink at themselves
    if receiver_id == request.user.id:
        data = {}
        data['message'] = "You can't wink at yourself, cheeky!"
        return JsonResponse(data)
        
    # Check if last wink send by request.user and received by recipient has been read
    current_wink = Winks.objects.filter(Q(receiver_id=receiver_id) & Q(sender_id=request.user.id) & Q(is_read=False)).exists()
    if current_wink:
        data = {}
        data['message'] = "Member hasn't viewed your last wink yet"
        return JsonResponse(data)
    
    # Create wink record
    wink = Winks(receiver=User.objects.get(pk=receiver_id), sender=request.user)
    data = {}
    try:
        wink.save()
    except:
        data['message'] = 'Something went wrong. Wink not sent'
    finally:
        data['message'] = 'Wink successfully sent.'
    return JsonResponse(data)

"""
AJAX function to create reject record. Used for quick match feature so as not to 
display a rejected user again
"""
def reject(request):
    # Get id of reject recipient
    receiver_id = request.GET.get('receiver_id')
    if receiver_id == request.user.id:
        return HttpResponse(status=204)
    
    # Check if a reject record for these users already exists, if so do nothing
    current_reject = Winks.objects.filter(Q(receiver_id=receiver_id) & Q(sender_id=request.user.id)).exists()
    if current_reject:
        return HttpResponse(status=204)
    
    # Create reject record
    reject = Reject(receiver=User.objects.get(pk=receiver_id), sender=request.user)
    data = {}
    try:
        reject.save()
    except:
        data['message'] = 'Something went wrong. Profile not skipped.'
    finally:
        data['message'] = 'Member successfully skipped'
    return JsonResponse(data)
        
# AJAX function to create a messages/conversation record(s)
@login_required
@premium_required
def chat_ajax(request):
    # Get message recipient and message content
    receiver_id = request.POST.get('message_receiver')
    message_content = request.POST.get('message_content')
    
    # If user tries to send a message to themselves
    if receiver_id == request.user.id:
        data = {}
        data['message'] = "You can't send a message to yourself"
        return JsonResponse(data)
    
    conversation = Conversations.objects.filter(participants=request.user.id).filter(participants=receiver_id)
    # If a conversation already exists between these two users, just create a message record
    if conversation.exists():
        try:
            message = Messages(
            receiver=User.objects.get(pk=receiver_id),
            sender=request.user,
            message_content=message_content,
            is_read=False,
            conversation=conversation[0]
            )
            message.save()
            data = {}
            data['message'] = "Message Successfully Sent"
            return JsonResponse(data)
        except:
            data = {}
            data['message'] = "Error occurred. Message not sent"
            return JsonResponse(data)
    # If a conversation doesn't exists, create a message and conversation record
    else:
        try:
            # Create conversation
            conversation = Conversations()
            conversation.save()
            conversation.participants.add(request.user)
            conversation.participants.add(User.objects.get(pk=receiver_id))
            # Create message
            message = Messages(
                receiver=User.objects.get(pk=receiver_id),
                sender=request.user,
                message_content=message_content,
                is_read=False,
                conversation=conversation
                )
            message.save()
            data = {}
            data['message'] = "Message Successfully Sent"
            return JsonResponse(data)
        except:
            data = {}
            data['message'] = "Error occurred. Message not sent"
            return JsonResponse(data)

# Winks page to display recieved winks
@login_required
def winks(request):
    
    # Query recieved winks and paginate results
    # Assistance from https://docs.djangoproject.com/en/1.11/topics/pagination/
    winks = Winks.objects.filter(receiver=request.user.id).order_by('-created_on')
    winks_paginated = Paginator(winks, 6)

    page = request.GET.get('page')
    try:
        winks_page = winks_paginated.page(page)
    except PageNotAnInteger:
        winks_page = winks_paginated.page(1)
        page = 1
    except EmptyPage:
        winks_page = winks_paginated.page(winks_paginated.num_pages)
        page = winks_paginated.num_pages
        
    
    context = {
        'page_ref': 'wink',
        'winks_page': winks_page,
        'page': page
    }
    
    
    return render(request, 'winks.html', context)
    
# Views page to display recieved views
@login_required
@premium_required   
def views(request):
    
    # Query recieved winks and paginate results
    views = Views.objects.filter(receiver=request.user.id).order_by('-created_on')
    views_paginated = Paginator(views, 6)
    
    page = request.GET.get('page')
    try:
        views_page = views_paginated.page(page)
    except PageNotAnInteger:
        views_page = views_paginated.page(1)
        page = 1
    except EmptyPage:
        views_page = views_paginated.page(views_paginated.num_pages)
        page = views_paginated.num_pages
        
    context = {
        'page_ref': 'view',
        'views_page': views_page,
        'page': page
    }
    
    return render(request, 'views.html', context)

# AJAX function to read all winks currently on specific page
@login_required
def read_wink(request):
    
    page = request.GET.get('page', None)
    
    winks = Winks.objects.filter(receiver=request.user.id).order_by('-created_on')
    winks_paginated = Paginator(winks, 6)
    
    try:
        winks_page = winks_paginated.page(page)
    except PageNotAnInteger:
        winks_page = winks_paginated.page(1)
    except EmptyPage:
        winks_page = winks_paginated.page(winks_paginated.num_pages)
    
    for wink in winks_page:
        wink.is_read = True
        wink.save()
        
    return HttpResponse(status=204)

# AJAX function to read all views currently on specific page
@login_required
@premium_required
def read_view(request):
    page = request.GET.get('page', None)
    
    views = Views.objects.filter(receiver=request.user.id).order_by('-created_on')
    views_paginated = Paginator(views, 6)
    
    try:
        views_page = views_paginated.page(page)
    except PageNotAnInteger:
        views_page = views_paginated.page(1)
    except EmptyPage:
        views_page = views_paginated.page(views_paginated.num_pages)
    
    for view in views_page:
        view.is_read = True
        view.save()
        
    return HttpResponse(status=204)