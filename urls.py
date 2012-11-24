from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from views import *

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'accelera.views.home', name='home'),
    url(r'^data/$', 'accelera.views.data', name='data'),
    url(r'^sse/$', MySseEvents.as_view(), name='sse'),
    # url(r'^accelera/', include('accelera.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)


urlpatterns += staticfiles_urlpatterns()
