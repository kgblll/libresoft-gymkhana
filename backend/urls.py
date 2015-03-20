#
#  Copyright (C) 2010 GSyC/LibreSoft, Universidad Rey Juan Carlos
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
#    Author : Roberto Calvo Palomino <rocapal_at_librsoft_dot_es>        
#


from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import direct_to_template

from views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
        '',

	(r'^$', init),
    (r'^login/$', login),
    
    (r'^home/$', home),
    
    (r'^layers/$', layers),
    (r'^layers/(?P<layer_id>[1-9][0-9]*)/$', get_layers_content), 
    (r'^layers/delete/$', layers_delete),    
    
    (r'^layers/(?P<layer_id>[1-9][0-9]*)/node/(?P<node_id>[1-9][0-9]*)/delete/$', delete_node), 
    
    (r'^contents/$', contents),
    (r'content/note/create/$', note_create),
    (r'content/photo/create/$', photo_create),
    (r'content/sound/create/$', sound_create),
    
)
