from django.conf.urls.defaults import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from views import MySseEvents

urlpatterns = patterns('',
    url(r'^$', 'accelera.views.home', name='home'),
    url(r'^sse/$', MySseEvents.as_view(), name='sse'),
)

urlpatterns += staticfiles_urlpatterns()
