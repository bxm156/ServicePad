from django.conf.urls.defaults import *

urlpatterns = patterns('ServicePad.apps.pages.views',
    (r'^$', 'index'),
    (r'^users/(?P<user_id>[0-9]+)/$','public_profile')
)
