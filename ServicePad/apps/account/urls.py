from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to

urlpatterns = patterns('ServicePad.apps.account.views',
    (r'^$', 'index'),
    (r'^messages/', include('ServicePad.apps.messages.urls')),
    (r'^teams/$','teams'),
    (r'^profile/$','profile'),
    (r'^events/$','events'),
    (r'availability/remove/(?P<a_id>[0-9]+)$','availability_remove'),
    (r'availability/$','availability'),
    (r'^logout/$','logout')
)
