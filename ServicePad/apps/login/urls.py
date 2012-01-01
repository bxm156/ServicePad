from django.conf.urls.defaults import patterns

urlpatterns = patterns('ServicePad.apps.login.views',
    (r'^$', 'login'),
)
