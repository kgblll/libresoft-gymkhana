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
#    Author : Jose Antonio Santos Cadenas <jcaden __at__ gsyc __dot__ es>
#

from django.shortcuts import render_to_response

from social.core import api

def group_map (request, group, template="test/group_map.html"):
    elements=api.group.get_group_elements(group)
    group = api.group.get_data(group)        
    positions=[]
    for key in elements.keys():
        for elem in elements[key]:
            positions.append(elem["position"])
    return render_to_response(template, {"positions":positions, 
                                         "group": group})
    
def groups_map (request, template="test/groups_map.html"):
    groups=api.group.get_all()
    to_delete = []
    for group in groups:
        if group["type"] == "dyngroup":
            elements=api.group.get_group_elements(group["id"])
            #group = api.group.get_data(group)        
            positions=[]
            for key in elements.keys():
                for elem in elements[key]:
                    positions.append(elem["position"])
            group["positions"] = positions
            pass
        else:
            to_delete.append(group)
            pass
    for delete in to_delete:
        groups.remove(delete)
    return render_to_response(template, {"groups": groups})
