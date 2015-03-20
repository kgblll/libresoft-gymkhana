# -*- coding: utf-8 -*-
#
#  Copyright (C) 2009-20010 Universidad Rey Juan Carlos, GSyC/LibreSoft
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

from format.utils import  getResponseFormat, generateResponse
from utils import error
from social.core.privacy import get_permissions as privacy_get_permissions
from social.core.privacy import privacy_change  
from social.core.privacy import get_all_roles, get_permissions_names

def privacy(request, node_id=None):
    format = getResponseFormat (request)
    if not request.user.is_authenticated():
        return error(format, "The user is not authenticated")
    if node_id == None:
        node_id = request.user.id
    success, perm = privacy_get_permissions(request.user.id, node_id)
    if success:
        data = {'code'         : '200',
                'privacy' : perm}
        return generateResponse(format, data, "privacy/privacy")
    else:
        return error(format, perm)

def change_privacy(request, node_id=None):
    
    format = getResponseFormat (request)
    if not request.user.is_authenticated():
        return error(format, "The user is not authenticated")
    if request.method != "POST":
        return error(format, "Need a POST petition")
    if node_id == None:
        node_id = request.user.id
    if "perm" in request.POST:
        perm = request.POST["perm"]
    else:
        perm = None
    if "field" in request.POST:
        field = request.POST["field"]
    else:
        field = None
        
    success, status = privacy_change(user_id=request.user.id, node_id=node_id, 
                                                 perm=perm, field = field)
    if success:
        data = {'code'             : '200',
                'description'      : "Permissions updated correctly"}
        return generateResponse(format, data, "ok")
    else:
        return error(format, status)


def get_roles(request):
    format = getResponseFormat (request)
    if not request.user.is_authenticated():
        return error(format, "The user is not authenticated")
    roles = get_all_roles()
    data = {'code'         : '200',
            'roles'        : roles}
    return generateResponse(format, data, "privacy/roles")

def get_permissions(request):
    format = getResponseFormat (request)
    if not request.user.is_authenticated():
        return error(format, "The user is not authenticated")
    roles = get_permissions_names()
    data = {'code'         : '200',
            'roles'        : roles}
    return generateResponse(format, data, "privacy/roles")
