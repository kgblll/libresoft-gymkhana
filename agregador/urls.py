from django.conf.urls.defaults import *
from agregador.views import join_rss_content

urlpatterns = patterns('',
#    (r'^type/(11870)/x/(.+)/y/(.+)/r/(.+)/text/(.*)$', join_rss_content),
    (r'^rest/$', join_rss_content),
)
