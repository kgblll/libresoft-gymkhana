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

from config import *

from django.contrib.contenttypes.models import ContentType

from models import Allowed_fields, Restricted_fields
from models import Allowed_objects, Restricted_objects

def is_privatizable(obj, field=None):
    """
    Checks the object and the field (if given) with the config file.
    
    @param obj: The object that must be in config file
    @param field: A field (or fields group name)
    
    @return: True if the data provided can use privacy application as it is
             written in config file.
    """
    if field==None:
        return obj.__module__ in privacy and obj.__class__.__name__ in privacy[obj.__module__]
    else:
        return obj.__module__ in privacy and \
               obj.__class__.__name__ in privacy[obj.__module__] and \
               field in privacy[obj.__module__][obj.__class__.__name__] and field != "basic"

def is_allowed(obj, role):
    """
    Checks if the role can be used to allow fields
    """
    try:
        o = ContentType.objects.get_for_model(obj)
        obj_allowed = Allowed_objects.objects.get(content_type__pk=o.id,
                                                  object_id=obj.id)
        return obj_allowed.allowed_roles.filter(id=role.id).count() > 0
    except:
        return False

def is_restricted(obj, role):
    """
    Checks if the role can be used to restrict fields
    """
    try:
        o = ContentType.objects.get_for_model(obj)
        obj_restricted = Restricted_objects.objects.get(content_type__pk=o.id,
                                                        object_id=obj.id)
        return obj_restricted.restricted_roles.filter(id=role.id).count() > 0
    except:
        return False

def get_groups(obj):
    """
    Return all the groups specified in the config file for an object
    """
    if is_privatizable(obj):
        fields=privacy[obj.__module__][obj.__class__.__name__].keys()
        try:
            fields.remove("basic")
        except ValueError:
            pass
        return fields
    else:
        return []
    
def get_allways_public_groups(obj):
    """
    Returns the always public fields groups for the object
    
    @param obj: The object
    
    @return: The always public fields groups for the requested object,
             None if no entry in the object database
    """
    if is_privatizable(obj):
        try:
            groups= always_public[obj.__module__][obj.__class__.__name__]
            final=[]
            for g in groups:
                if g in get_groups(obj):
                    final.append(g)
            return final
        except:
            return None
    else:
        return None
    