from django.conf.urls.defaults import patterns

urlpatterns = patterns('ServicePad.apps.events.views',
    (r'^$', 'login'),
    (r'^create/$','create')
)
