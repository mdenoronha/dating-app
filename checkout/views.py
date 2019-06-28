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

# Check redirect reverse are working
# Create your views here.

stripe.api_key = settings.STRIPE_SECRET

def make_user_premium(request):
    profile = Profile.objects.get(user_id=request.user.id)
    profile.is_premium = True
    profile.save()
    
    return

@login_required
def subscribe(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        payment_form = MakePaymentForm(request.POST)
        if order_form.is_valid() and payment_form.is_valid():
            order = order_form.save(commit=False)
            order.date = timezone.now()
            order.save()
            
            print(order.plans)
            
            customer = stripe.Customer.list(email=request.user.email)
            # customer = Subscription.objects.filter(user_id=request.user.id).first()
            # If customer already exists
            if customer:
                """
                Stripe returns a list of customers, as there shouldn't be any more
                one customer from a email query, the first of the list is used. If
                more than one is returned, the latest active account would be used.
                """
                active_customer = customer.data[0]
                # Merge into one try
                try:
                    print("updating customer")
                    stripe.Customer.modify(
                        active_customer.id,
                        card = payment_form.cleaned_data['stripe_id']
                    )
                # Add error messages
                except:
                    print('error')
                    return redirect(reverse('checkout'))
                    
                try:
                    print("updating sub")
                    stripe.Subscription.create(
                        customer = active_customer.id,
                        items=[{"plan": order.plans,},]
                    )
                except stripe.error.CardError:
                    messages.error(request, "Your card was declined!")
                    return redirect(reverse('checkout'))
                finally:
                    subscription = Subscription(
                            user = request.user, 
                            plan = "Monthly", 
                            customer_id = active_customer.id
                            )
                    subscription.save()
                    make_user_premium(request)
            else:
            # If new customer
                try:
                    customer = stripe.Customer.create(
                        email = request.user.email,
                        plan = order.plans,
                        description = request.user.email,
                        card = payment_form.cleaned_data['stripe_id'],
                    )
                except stripe.error.CardError:
                    messages.error(request, "Your card was declined!")
                    return redirect(reverse('checkout'))
                
                finally:
                # Add check if subscription created successfully (will need to change paid
                # https://stripe.com/docs/api/customers/create)
                # if customer.paid:
                #     messages.error(request, "You have paid successfully")
                #     return redirect(reverse('index'))
                    subscription = Subscription(
                            user = request.user, 
                            # Make custom
                            plan = "Monthly", 
                            customer_id = customer.id
                            )
                    subscription.save()
                    make_user_premium(request)
                
                # else:
                #     messages.error(request, "Unable to take payment")
        else:
            messages.error(request, "Unable to take payment")
            print(order_form.errors)
            print(payment_form.errors)
    else:
        payment_form = MakePaymentForm()
        order_form = OrderForm()
      
    return render(request, 'subscribe.html', {'order_form': order_form, 'payment_form': payment_form, 'publishable': settings.STRIPE_PUBLISHABLE})

