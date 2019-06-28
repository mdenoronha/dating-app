from django.conf.urls import url, include
from search.views import search

urlpatterns = [
    url(r'^$', search, name="search"),
]
