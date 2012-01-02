from django.conf.urls.defaults import *

urlpatterns = patterns('ServicePad.apps.pages.views',
    (r'^$', 'index')
)
