from django.conf.urls.defaults import patterns

urlpatterns = patterns('ServicePad.apps.bookmarks.views',
    (r'^(?P<eid>[0-9]+)/?$', 'bookmark'),
    (r'^remove/(?P<eid>[0-9]+)/?$', 'remove_bookmark')
)
