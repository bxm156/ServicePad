from django.conf.urls.defaults import patterns

urlpatterns = patterns('ServicePad.apps.events.views',
    (r'^(?P<id>[0-9]+)/?$', 'view'),
    (r'^(?P<event_id>[0-9]+)/join?$', 'join'),
    (r'^create/?$','create'),
	(r'^', 'list')
)
