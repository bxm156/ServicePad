from django.conf.urls.defaults import patterns

urlpatterns = patterns('ServicePad.apps.messages.views',
    (r'^(?P<message_id>[0-9]+)/?$', 'message'),
    (r'^compose/?$','compose'),
	(r'^', 'inbox')
)
