from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from .forms import OrderForm, MakePaymentForm
from .models import Subscription
from django.utils import timezone
import stripe
from profiles.models import Profile


stripe.api_key = settings.STRIPE_SECRET

# Function to update user profile to premium
def make_user_premium(request):
    profile = Profile.objects.get(user_id=request.user.id)
    profile.is_premium = True
    profile.save()
    
    return

# Subscribe page, allowing users to create a Stripe subscription
@login_required
def subscribe(request):
    plan_ids = {
        'plan_F5eyNlWXHig7YB': '6 Monthly',
        'plan_F5ey2nnZwy5v8Q': '3 Monthly',
        'plan_F5eyGdYCvZPtON': 'Monthly'
    }
    
    # If user submits payment form
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        payment_form = MakePaymentForm(request.POST)
        if order_form.is_valid() and payment_form.is_valid():
            order = order_form.save(commit=False)
            order.date = timezone.now()
            order.save()
            
            subscription = Subscription.objects.filter(user_id=request.user.id).first()
            
            # If user has subscribed before and has customer record
            if subscription:
                customer = stripe.Customer.retrieve(subscription.customer_id)

                try:
                    stripe.Customer.modify(
                        customer.id,
                        card = payment_form.cleaned_data['stripe_id']
                    )
                except:
                    messages.error(request, "Error updating your customer record")
                    return redirect(reverse('subscribe'))
                    
                try:
                    stripe.Subscription.create(
                        customer = customer.id,
                        items=[{"plan": order.plans,},]
                    )
                except stripe.error.CardError:
                    messages.error(request, "Your card was declined!")
                    return redirect(reverse('subscribe'))
                finally:
                    # Create new subscription
                    subscription = Subscription(
                            user = request.user, 
                            plan = plan_ids[order.plans], 
                            customer_id = customer.id
                            )
                    subscription.save()
                    make_user_premium(request)
                    messages.error(request, "Success! You are now a premium user")
                    return redirect(reverse('index'))
            # If user has not subscribed before and has no customer record
            else:
                try:
                    customer = stripe.Customer.create(
                        email = request.user.email,
                        plan = order.plans,
                        description = request.user.email,
                        card = payment_form.cleaned_data['stripe_id'],
                    )
                except stripe.error.CardError:
                    messages.error(request, "Your card was declined!")
                    return redirect(reverse('subscribe'))
                finally:
                # Assistance from https://stripe.com/docs/api/customers/create
                    subscription = Subscription(
                            user = request.user, 
                            plan = plan_ids[order.plans], 
                            customer_id = customer.id
                            )
                    subscription.save()
                    make_user_premium(request)
                    messages.error(request, "Success! You are now a premium user")
                    return redirect(reverse('index'))
        else:
            messages.error(request, "Unable to take payment")
    else:
        payment_form = MakePaymentForm()
        order_form = OrderForm()
      
    return render(request, 'subscribe.html', {'page_ref': 'subscribe', 'order_form': order_form, 'payment_form': payment_form, 'publishable': settings.STRIPE_PUBLISHABLE})

