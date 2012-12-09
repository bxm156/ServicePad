from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ServicePad.views.home', name='home'),
    # url(r'^ServicePad/', include('ServicePad.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    (r'', include('ServicePad.apps.pages.urls')),
    (r'^events/', include('ServicePad.apps.events.urls')),
    (r'^service/', include('ServicePad.apps.service.urls')),
    (r'^account/', include('ServicePad.apps.account.urls')),
    (r'^teams/', include('ServicePad.apps.team.urls')),
    (r'^bookmark/', include('ServicePad.apps.bookmarks.urls')),
    (r'^register/', include('ServicePad.apps.registration.urls')),
    (r'^login/', include('ServicePad.apps.login.urls')),
)
