from django.conf.urls.defaults import *

urlpatterns = patterns('ServicePad.apps.team.views',
    (r'^$', 'list'),
    (r'^create/$', 'create'),
    (r'^(?P<id>[0-9]+)/?$', 'view'),
)
