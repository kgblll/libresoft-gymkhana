#
#  Copyright (C) 2009 GSyC/LibreSoft
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
#    Author : Jose Gato Luis <jgato __at__ libresoft __dot__ es>
#

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^semantic/similarity/words/$', 'apps.semanticSearch.views.similarityWords', name="similarSemantic"),
    url(r'^social/search/semantic/$', 'apps.semanticSearch.views.socialSearchSemantic', name="socialSemanticSearch"),
    url(r'^social/node/distances/$', 'apps.semanticSearch.views.compareSemanticNodes', name="compareNodesSemantic"),
    url(r'^social/node/(?P<node_id1>[1-9][0-9]*)/distance/(?P<node_id2>[1-9][0-9]*)/$', 'apps.semanticSearch.views.compareTwoSemanticNodes',name="compareTwoNodesSemantic")



)

