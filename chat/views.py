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
# error message checks needed

@login_required
@premium_required
def new_message_check(request):
    conversation_id = request.GET.get('url_id', None)
    is_read = Messages.objects.filter(conversation=conversation_id, receiver=request.user, is_read=False).exists()
    data = {
        'conversation': is_read
    }
    return JsonResponse(data)
    
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

@login_required
@premium_required
def chat(request, id):
    
    conversation_ids = Conversations.objects.filter(participants=request.user)

    all_conversations = {}
    is_read_check = {}
    for conversation in conversation_ids:  
        all_conversations[conversation.id] = Messages.objects.filter(conversation=conversation).last()

        # Make one db query
        if Messages.objects.filter(conversation=conversation, receiver=request.user).last():
            last_received_message = Messages.objects.filter(conversation=conversation, receiver=request.user).last() 
            is_read_check[conversation.id] = last_received_message.is_read
        else: 
            is_read_check[conversation.id] = True
    
    messages = Messages.objects.filter(conversation=id)
        
    conversation = Conversations.objects.get(pk=id)
    participants = conversation.participants.all()
    for user in participants:
        if not user.id == request.user.id:
            receiver = user
        
    if request.method == "POST":
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            if receiver.id == request.user.id:
                messages.success(request, "You can't send a message to yourself")
                return redirect(reverse('chat_home'))
            
            message = message_form.save(commit=False)
            message.receiver = User.objects.get(id=receiver.id)
            message.sender = request.user
            message.conversation = conversation
            message.save()
            
        context = {
            'user_messages': messages,
            'message_form':message_form,
            'all_conversations': all_conversations,
            'receiver': receiver,
            'conversation_id': int(id),
            'is_read_check': is_read_check
        }
        return HttpResponseRedirect("/chat/%s" % id)
    else:
        message_form = MessageForm()
    
    page_ref = "chat"
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
  
@login_required  
@premium_required 
def chat_home(request):
    conversation_ids = Conversations.objects.filter(participants=request.user)

    all_conversations = {}
    is_read_check = {}
    for conversation in conversation_ids:  
        all_conversations[conversation.id] = Messages.objects.filter(conversation=conversation).last()

        # Make one db query
        if Messages.objects.filter(conversation=conversation, receiver=request.user).last():
            last_received_message = Messages.objects.filter(conversation=conversation, receiver=request.user).last() 
            is_read_check[conversation.id] = last_received_message.is_read
        else: 
            is_read_check[conversation.id] = True

    context = {
        'user_messages': messages,
        'all_conversations': all_conversations,
        'conversation_id': None,
        'is_read_check': is_read_check
    }

    return render(request, 'chat_home.html', context)
    
# Get rid of?
def create(request):
    
    # message_form = MessageForm()
    
    if request.method == "POST":
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            conversation = Conversations()
            conversation.save()
            conversation.participants.add(request.user, 39)

            message = message_form.save(commit=False)
            message.receiver = User.objects.get(id=2)
            message.sender = request.user
            message.save()
    else:
        message_form = MessageForm()
        
    context = {
        'message_form': message_form
    }
    
    return render(request, 'create.html', {'message_form':message_form})

def wink(request):
    # Change None backup?
    receiver_id = request.GET.get('receiver_id')
    if receiver_id == request.user.id:
        messages.success(request, "You can't send a wink to yourself, cheeky")
        return redirect(reverse('index'))
    current_wink = Winks.objects.filter(Q(receiver_id=receiver_id) & Q(sender_id=request.user.id) & Q(is_read=False)).exists()
    if current_wink:
        # messages.success(request, "Your last wink hasn't been seen yet. Try again later.")
        print("not seen")
        return HttpResponse(status=204)
    
    wink = Winks(receiver=User.objects.get(pk=receiver_id), sender=request.user)
    try:
        wink.save()
    except:
        # messages.success(request, "Something went wrong. Wink not sent")
        print("not sent")
    finally:
        # messages.success(request, "Wink successfully sent.")
        print("sent")
    # pass messages using https://stackoverflow.com/questions/52483675/how-to-filter-django-annotations-on-reverse-foreign-key-fields
    return HttpResponse(status=204)
    
def reject(request):
    # Change None backup?
    receiver_id = request.GET.get('receiver_id')
    if receiver_id == request.user.id:
        return HttpResponse(status=204)
        
    current_reject = Winks.objects.filter(Q(receiver_id=receiver_id) & Q(sender_id=request.user.id)).exists()
    if current_reject:
        return HttpResponse(status=204)
    
    reject = Reject(receiver=User.objects.get(pk=receiver_id), sender=request.user)
    try:
        reject.save()
    except:
        # messages.success(request, "Something went wrong. Reject not sent")
        print("Error Occurred")
    finally:
    # pass messages using https://stackoverflow.com/questions/52483675/how-to-filter-django-annotations-on-reverse-foreign-key-fields
        return HttpResponse(status=204)

@login_required
@premium_required
def chat_ajax(request):
    receiver_id = request.POST.get('message_receiver')
    message_content = request.POST.get('message_content')
    
    if receiver_id == request.user.id:
        messages.success(request, "You can't send a message to yourself")
        return redirect(reverse('index'))
    
    conversation = Conversations.objects.filter(participants=request.user.id).filter(participants=receiver_id)
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
        except:
            # Errors
            print("Error report")
    else:
        try:
            conversation = Conversations()
            conversation.save()
            # Is this working?
            conversation.participants.add(request.user.id)
            conversation.participants.add(User.objects.get(pk=receiver_id))
            message = Messages(
                receiver=User.objects.get(pk=receiver_id),
                sender=request.user,
                message_content=message_content,
                is_read=False,
                conversation=conversation
                )
            message.save()
        except:
            # Errors
            print("Error report")
            
    return HttpResponse(status=204)
    
@login_required
def winks(request):
    
    winks = Winks.objects.filter(receiver=request.user.id).order_by('-created_on')
    winks_paginated = Paginator(winks, 6)

    page = request.GET.get('page')
    # https://docs.djangoproject.com/en/1.11/topics/pagination/
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

@login_required
@premium_required   
def views(request):

    views = Views.objects.filter(receiver=request.user.id).order_by('-created_on')
    views_paginated = Paginator(views, 6)

    page = request.GET.get('page')
    # https://docs.djangoproject.com/en/1.11/topics/pagination/
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