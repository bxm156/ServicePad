from django.conf.urls.defaults import *

urlpatterns = patterns('ServicePad.apps.team.views',
    (r'^$', 'list'),
    (r'^create/$', 'create'),
    (r'^(?P<id>[0-9]+)/$', 'view'),
    (r'^(?P<team_id>[0-9]+)/accept/$', 'accept'),
    (r'^(?P<team_id>[0-9]+)/decline/$', 'decline'),
    (r'^(?P<team_id>[0-9]+)/admin/$', 'admin'),
)
