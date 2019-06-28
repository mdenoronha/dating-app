from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from checkout.models import Subscription
from django.contrib import messages
from django.contrib.auth.models import User
from profiles.models import Profile
from django.contrib.auth import update_session_auth_hash
import stripe
import datetime
from datetime import timedelta  
import time
from django.contrib.auth.forms import PasswordChangeForm
from profiles.forms import EditProfileForm
# Create your views here.

@login_required
def account(request):
    
    def return_subs():
        
        customer_id = Subscription.objects.filter(user_id=request.user).first()
        if customer_id:
            customer_id = customer_id.customer_id
            # customer = stripe.Customer.list(email=request.user.email)
            customer = stripe.Customer.retrieve(customer_id)
        
            subscriptions = []
            for sub in customer.subscriptions.data:
                subscriptions.append(sub)
            
            if customer:
                # Filters old subscriptions 
                active_subscriptions = [sub for sub in subscriptions if sub.created < time.time()]
                
                for sub in active_subscriptions:
                    sub.created = datetime.datetime.fromtimestamp(float(sub.created))
                    sub.current_period_end = datetime.datetime.fromtimestamp(float(sub.current_period_end))
            else:
                customer = {}
                active_subscriptions = {}
                customer_id = None
            
        else:
            customer = {}
            active_subscriptions = {}
            customer_id = None
        
        return active_subscriptions, customer, customer_id
    
    if request.method == "POST" and 'account-change-submit' in request.POST:
        password_form = PasswordChangeForm(request.user)
        user_form = EditProfileForm(request.POST, instance=request.user, user=request.user)
        
        if user_form.is_valid():
            active_subscriptions, customer, customer_id = return_subs()
            profile = Profile.objects.get(pk=request.user)
            profile.is_verified = "TO BE APPROVED"
            user_form.save()
            if customer_id:
                stripe.Customer.modify(customer_id, email=user_form.cleaned_data['email'])
        else:
            user = User.objects.get(pk=request.user.id)
            request.user = user
            active_subscriptions, customer, customer_id = return_subs()
    
    elif request.method == "POST" and 'password-change-submit' in request.POST:
            user_form = EditProfileForm(instance=request.user, user=request.user)
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)
                active_subscriptions, customer, customer_id = return_subs()
            else:
               active_subscriptions, customer, customer_id = return_subs() 
    else:
        user_form = EditProfileForm(instance=request.user, user=request.user)
        password_form = PasswordChangeForm(request.user)
        active_subscriptions, customer, customer_id = return_subs()
     
        
    context = {
        'password_form': password_form,
        'user_form': user_form,
        'customer': customer,
        'active_subscriptions': active_subscriptions
    }
    
    return render(request, 'account.html', context)

@login_required   
def cancel_subscription(request, subscription_id):
    
    # Check if subscription belows to user
    subscription = Subscription.objects.filter(user_id=request.user).first()
    active_subscription = stripe.Subscription.retrieve(subscription_id)
    if active_subscription.customer != subscription.customer_id:
        messages.error(request, "Authentication failed")
        return redirect(reverse('account'))
    
    try:
        stripe.Subscription.modify(
            subscription_id,
            cancel_at_period_end=True
        )
    except Exception:
        messages.error(request, "Cancellation failed")
        
    return redirect(reverse('account'))
    
@login_required   
def reactivate_subscription(request, subscription_id):
    
    subscription = Subscription.objects.filter(user_id=request.user).first()
    active_subscription = stripe.Subscription.retrieve(subscription_id)
    if active_subscription.customer != subscription.customer_id:
        messages.error(request, "Authentication failed")
        return redirect(reverse('account'))
    
    try:
        stripe.Subscription.modify(
            subscription_id,
            cancel_at_period_end=False
        )
    except Exception:
        messages.error(request, "Cancellation failed")
        
    return redirect(reverse('account'))
    
