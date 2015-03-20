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
#    Author : Jose Gato Luis <jgato at libresoft dot es >
#

from django.template import Context, Library, loader
from django import template

from social.core.api import node 

register = Library()


@register.simple_tag
def display_search(result, format):
    ret=""

    type = result['info'][0]
    element = result['data']
    
    
    if format=="xml":
        ret += u"<%s>\n" % type
    elif format=="json":
        ret += u'"%s": [\n' % type
        ret += u"{\n"

    ret += u"%s" %element
                
    if format=="xml": 
        ret += u"</%s>\n" % type
    elif format=="json":
        ret += u"},\n"
        ret+='],\n'
    
    return ret

