from django.conf.urls.defaults import *

urlpatterns = patterns('ServicePad.apps.login.views',
    (r'^$', 'login'),
)
