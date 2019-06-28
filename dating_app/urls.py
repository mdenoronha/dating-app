"""dating_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin
from profiles import urls as profile_urls
from chat import urls as chat_urls
from home import urls as home_urls
from account import urls as account_urls
from checkout import urls as subscribe_urls
from search import urls as search_urls
from django.views.static import serve
from .settings import MEDIA_ROOT


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(home_urls)),
    url(r'accounts/', include(profile_urls)),
    url(r'chat/', include(chat_urls)),
    url(r'subscribe/', include(subscribe_urls)),
    url(r'my-account/', include(account_urls)),
    url(r'search/', include(search_urls)),
    url(r'media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}) 
    ]
