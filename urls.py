from django.conf.urls import patterns, include, url
import os
from os.path import join

from settings import MEDIA_ROOT, APPS_DIR, BASEDIR, INFOMEDIA_ROOT

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'lgs.views.home', name='home'),
    # url(r'^lgs/', include('lgs.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^version/', 'social.rest.views.version',),
    url(r'^social/',include('social.rest.urls'),),
    url(r'^backend/',include('backend.urls'),),
    url(r'^site_media/images/photos','social.rest.views.forbbiden_photo',),
    url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':MEDIA_ROOT}),
    url(r'^agregador/', include('agregador.urls'),),
    url(r'^infomedia/(?P<path>.*)$','django.views.static.serve',{'document_root':INFOMEDIA_ROOT}),
)


def look_up_apps():
    apps_dir = join(BASEDIR,APPS_DIR)
    print apps_dir
    dirs = os.listdir(apps_dir)
    pat = urlpatterns
    for dir in dirs:
        if os.path.isdir(join(apps_dir,dir)) and dir[0] not in ('.','_'):
            urls=r'^%s/' % dir
            urls_file='%s.%s.urls' % (APPS_DIR,dir)
            pat= pat + patterns('',(urls,include(urls_file)))
    return pat




try:
    urlpatterns= look_up_apps()
except:
    pass
