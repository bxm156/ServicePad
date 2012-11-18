from django.conf.urls.defaults import patterns

urlpatterns = patterns('ServicePad.apps.bookmarks.views',
    (r'^(?P<id>[0-9]+)/?$', 'bookmark')
)
