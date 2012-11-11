from django.conf.urls.defaults import patterns
from ServicePad.settings import LOGIN_REDIRECT_URL
urlpatterns = patterns('',
   (r'^cas/$','django_cas.views.login',{'next_page':LOGIN_REDIRECT_URL}),
   (r'^$', 'django.contrib.auth.views.login',{'template_name':'login.html'}),
   #(r'^$', 'login'),
)
