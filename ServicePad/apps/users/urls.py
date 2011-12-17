from django.conf.urls.defaults import *

urlpatterns = patterns('ServicePad.apps.users.views',
    (r'^$', 'register'),
   #(r'^confirm/$','register')
)
