from .models import Subscription
import stripe
from django.shortcuts import render, redirect, reverse

def premium_required(function):
    def wrap(request, *args, **kwargs):
        
        if request.user.profile.is_premium:
            customer_stripe_id = Subscription.objects.filter(user_id=request.user).first()
            customer = stripe.Customer.retrieve(customer_stripe_id.customer_id)
            for sub in customer.subscriptions:
                    # If subscription is active or unpaid/cancelled but not yet inactive
                if sub.status == 'active' or sub.status == 'trialing' or sub.status == 'incomplete' or sub.status == 'past_due' or sub.status == 'canceled':
                    return function(request, *args, **kwargs)
            
            request.user.profile.is_premium = False
            return redirect(reverse('subscribe'))
        else:
            return redirect(reverse('subscribe'))
            
    # wrap.__doc__ = function.__doc__
    # wrap.__name__ = function.__name__
    return wrap
    

    
    