from django.conf.urls.defaults import *

urlpatterns = patterns('ServicePad.apps.service.views',
    (r'^review/(?P<enrollment_id>[0-9]+)/$','review')
)
