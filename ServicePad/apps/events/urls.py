from django.conf.urls.defaults import patterns

urlpatterns = patterns('ServicePad.apps.events.views',
    (r'^(?P<id>[0-9]+)/?$', 'view'),
    (r'^(?P<event_id>[0-9]+)/join/?$', 'join'),
    (r'^(?P<event_id>[0-9]+)/join/team/?$', 'join', {'show_teams':True}),
    (r'^(?P<event_id>[0-9]+)/join/team/(?P<team_id>[0-9]+)/?$', 'join', {'show_teams':True}),
    (r'^create/?$','create'),
	(r'^', 'list')
)
