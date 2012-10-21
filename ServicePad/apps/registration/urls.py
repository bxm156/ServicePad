from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to
from ServicePad.apps.account.models import UserProfile

urlpatterns = patterns('ServicePad.apps.registration.views',
    (r'^$', 'register', {'type':UserProfile.ACCOUNT_VOLUNTEER}),
    (r'^volunteer/$', 'register', {'type':UserProfile.ACCOUNT_VOLUNTEER}),
    (r'^organization/$', 'register', {'type':UserProfile.ACCOUNT_ORGANIZATION}),
    (r'^confirm/$',redirect_to, {'url': '/register', 'permanent': False}),
    (r'^confirm/(?P<user>[0-9]+)/(?P<key>[a-zA-Z0-9]{32})/$','confirm')
)
