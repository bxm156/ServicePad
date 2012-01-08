from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
   (r'^$', 'django.contrib.auth.views.login',{'template_name':'login.html'}),
   #(r'^$', 'login'),
)
