from django.conf.urls import url, include
from profiles.views import logout, login, register, user_profile, create_profile, validate_username, member_profile
from profiles import url_reset

urlpatterns = [
    url(r'^logout/', logout, name='logout'),
    url(r'^login/', login, name='login'), 
    url(r'^register/', register, name='register'),
    url(r'^create-profile/', create_profile, name='create_profile'),
    url(r'^edit/', user_profile, name="user_profile"),
    url(r'^member/(?P<id>\d+)', member_profile, name='member_profile'),
    url(r'^ajax/validate_username/$', validate_username, name='validate_username'),
    url(r'^password-reset/', include(url_reset))
]