from django.contrib import admin
from .models import Order, Subscription

# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    model = Order

class SubscriptionAdmin(admin.ModelAdmin):
    model = Subscription
    list_display = 'user', 'plan'
    
admin.site.register(Order, OrderAdmin)
admin.site.register(Subscription, SubscriptionAdmin)

