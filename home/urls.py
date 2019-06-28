from django.conf.urls import url
from .views import index, preregister

urlpatterns = [
    url(r'^$', preregister, name='preregister'),
    url(r'^home/', index, name="index"),
]
