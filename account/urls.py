from django.conf.urls import url
from .views import account, cancel_subscription, reactivate_subscription

urlpatterns = [
    url(r'^$', account, name='account'),
    url(r'^cancel/(?P<subscription_id>[0-9A-Za-z_]+)$', cancel_subscription, name='cancel_subscription'),
    url(r'^reactivate/(?P<subscription_id>[0-9A-Za-z_]+)$', reactivate_subscription, name='reactivate_subscription')]