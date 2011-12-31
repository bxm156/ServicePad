from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to

urlpatterns = patterns('ServicePad.apps.users.views',
    (r'^$', 'register'),
    (r'^confirm/$',redirect_to, {'url': '/register', 'permanent': False}),
    (r'^confirm/(?P<user>[0-9]+)/(?P<key>[a-zA-Z0-9]{32})/$','confirm')
)
