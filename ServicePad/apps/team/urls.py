from django.conf.urls.defaults import *

urlpatterns = patterns('ServicePad.apps.team.views',
    (r'^$', 'index'),
    (r'^create/$', 'create'),
    (r'^(?P<id>[0-9]+)/?$', 'view'),
)
