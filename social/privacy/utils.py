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

from models import Allowed_fields, Restricted_fields
from models import Allowed_objects, Restricted_objects
from models import Character, Role, Function
from django.contrib.contenttypes.models import ContentType

import pickle

import __aux__ as aux

class Privacy(object):
    __access=None
    __fields_allowed=[]
    __fields_restricted=[]
    __object=None
    
    def __init__(self, *args, **kwargs):
        if "access" in kwargs:
            self.__access=kwargs["access"]
        if "allowed" in kwargs:
            self.__fields_allowed=kwargs["allowed"]
        if "restricted" in kwargs:
            self.__fields_restricted=kwargs["restricted"]
        if "object" in kwargs:
            self.__object=kwargs["object"]
                
    def get_allowed_fields(self):
        allowed=aux.get_allways_public_groups(self.__object)
        if allowed==None:
            if not self.__access:
                #No public object
                return None
            else:
                allowed=[]
        if "basic" not in allowed:
            allowed+=["basic"]
        allowed += self.__fields_allowed
        for field in self.__fields_restricted:
            if field in allowed:
                allowed.remove(field)
        return allowed
            
def is_allowed(req_obj, requester, field=None):
    """
    This functions return True if the requester is fully allowed at req_obj
    None if there is no data and False if is fully rejected
    
    @param req_obj: The requested object that will be checked
    @param requester: The user that wants to access to the req_obj
    @param field: An optional parameter field 
    """
    
    obj = ContentType.objects.get_for_model(req_obj)
    if field==None:
        #Check if has not access
        obj_restricted = Restricted_objects.objects.filter(content_type__pk=obj.id,
                                                           object_id=req_obj.id)
        for object in obj_restricted:
            for role in object.not_allowed_roles.all():
                if role.contains(req_obj, requester):
                    return False
        
        #Look if has access
        obj_allowed = Allowed_objects.objects.filter(content_type__pk=obj.id,
                                                     object_id=req_obj.id)
        for object in obj_allowed:
            for role in object.allowed_roles.all():
                if role.contains(req_obj, requester):
                    return True
    else:
        #Look for restricted fields
        obj_restricted_fields = Restricted_fields.objects.filter(content_type__pk=obj.id,
                                                              object_id=req_obj.id,
                                                              field_name=field)
        for field in obj_restricted_fields:
            for role in field.restricted_roles.all():
                #First check if the requester is in the list of allowed characters
                if role.contains(req_obj, requester):
                    return False

        #Look for allowed fields
        obj_allowed_fields = Allowed_fields.objects.filter(content_type__pk=obj.id,
                                                           object_id=req_obj.id,
                                                           field_name=field)
        for field in obj_allowed_fields:
            for role in field.allowed_roles.all():
                #First check if the requester is in the list of allowed characters
                if role.contains(req_obj, requester):
                    return True

    return None

def get_fields(req_obj, requester):
    """
    This function will return an array with the name of the allowed fields of req_obj
    for the requester user.
    
    @param req_obj: The requested object that will be checked
    @param requester: The user that wants to access to the req_obj  
    
    @return: An array with all the allowed fields, if the array is empty means
             that the requester has access to basic fields but no to other fields.
             If return None means no access to the object
    """
    allowed_fields=[]
    restricted_fields=[]
    full_access=False
    no_access=False
    
    obj = ContentType.objects.get_for_model(req_obj)
           
    #Look for allowed fields
    obj_allowed_fields = Allowed_fields.objects.filter(content_type__pk=obj.id,
                                                       object_id=req_obj.id)
    for field in obj_allowed_fields:
        allow=False
        for role in field.allowed_roles.all():
            #First check if the requester is in the list of allowed characters
            if role.contains(req_obj, requester):
                allow=True
                break
        if allow:
            allowed_fields+=[field.field_name]
            allow=False
        
    #Check if has no access to some field
    obj_restricted_fields = Restricted_fields.objects.filter(content_type__pk=obj.id,
                                                             object_id=req_obj.id)
    for field in obj_restricted_fields:
        restricted=False
        for role in field.not_allowed_roles.all():
            #First check if the requester is in the list of allowed characters
            if role.contains(req_obj, requester):
                restricted=True
                break
        if restricted:
            restricted_fields+=[field.field_name]
            restricted=False
    
    privacy=Privacy(allowed=allowed_fields, access=is_allowed(req_obj, requester),
                    restricted=restricted_fields, object=req_obj)
    return privacy.get_allowed_fields()
    
def get_object_status(req_obj):
    """
    This function provides informations about an object privacy.
    
    @param req_obj: The object
    
    @return: A dictionary with 2 arrays: "full", "forbidden"
             Both of them with the respective roles names
             And 2 dictionaries: "fields_allowed", "fields_restricted"
             With an entry for each field, containing an array
             with the allowed or restricted roles
    """
    response={"full":[], "forbidden": [], "fields_allowed": {},
              "fields_forbidden": {},}
    obj = ContentType.objects.get_for_model(req_obj)
    #Look for full access roles
    obj_allowed = Allowed_objects.objects.filter(content_type__pk=obj.id,
                                                 object_id=req_obj.id)
    for object in obj_allowed:
        response["full"]=[role.name for role in object.allowed_roles.all()]
        
     #Check if has not access to any field
    obj_restricted = Restricted_objects.objects.filter(content_type__pk=obj.id,
                                                       object_id=req_obj.id)
    for object in obj_restricted:
        response["forbidden"]=[role.name for role in object.not_allowed_roles.all()]
    
    #Create dictionaries with the fields
    for field in aux.get_groups(req_obj):
        response["fields_allowed"][field]=[]
        response["fields_forbidden"][field]= []
    response["fields_allowed"]["basic"]= response["full"]+[]
    response["fields_forbidden"]["basic"]=  response["forbidden"]+[]
    
    #Look for allowed fields
    obj_allowed_fields = Allowed_fields.objects.filter(content_type__pk=obj.id,
                                                       object_id=req_obj.id)
    for field in obj_allowed_fields:
        response["fields_allowed"][field.field_name] = [role.name for role in field.allowed_roles.all()]
        
    #Check if has no access to some field
    obj_restricted_fields = Restricted_fields.objects.filter(content_type__pk=obj.id,
                                                             object_id=req_obj.id)
    for field in obj_restricted_fields:
        response["fields_forbidden"][field.field_name] = [role.name for role in field.not_allowed_roles.all()]

    return response

def allow(obj, field_name, roles):
    """
    Allows the access to the field of the indicated object to the roles
    
    @param obj: The object
    @param field_name: The field name (using display_name)
    @param roles: An array with all the roles with permission for watching this field
    """
    if not aux.is_privatizable(obj, field_name):
        return False
    try:
        obj_type= ContentType.objects.get_for_model(obj)
        p=Allowed_fields.objects.get(content_type__pk=obj_type.id, 
                                     object_id=obj.id,
                                     field_name=field_name)
    except:
        p=Allowed_fields(element=obj, field_name=field_name)
        p.save()
    for role in roles:
        if role.combo:
            to_delete = p.allowed_roles.filter(combo=role.combo)
            for r in to_delete:
                p.allowed_roles.remove(r)
        p.allowed_roles.add(role)

def allow_undo(obj, field_name, roles):
    """
    Deletes the roles from the allowed roles 
    
    @param obj: The object
    @param field_name: The field name (using display_name) 
    @param roles: An array with all the roles that will be deleted from allowed roles
    """
    if not aux.is_privatizable(obj, field_name):
        return False
    try:
        obj_type= ContentType.objects.get_for_model(obj)
        p=Allowed_fields.objects.get(content_type__pk=obj_type.id, 
                                     object_id=obj.id,
                                     field_name=field_name)
        for role in roles:
            p.allowed_roles.remove(role)
    except:
        pass
    

def allow_undo_all_fields (obj, roles):
    """
    Deletes the roles from the allowed roles of all fields
    
    @param obj: The object
    @param roles: An array with all the roles that will be deleted from the allowed roles
    """
    if not aux.is_privatizable(obj):
        return False
    try:
        obj_type= ContentType.objects.get_for_model(obj)
        fields=Allowed_fields.objects.filter(content_type__pk=obj_type.id, 
                                             object_id=obj.id)
        for field in fields:
            for role in roles:
                field.allowed_roles.remove(role)
    except:
        pass

#TODO: Review restrict and restrict all now works like allow, but I think it's a little bit different.
def restrict(obj, field_name, roles):
    """
    Restricts the access to the field of the indicated object to the roles
    
    @param obj: The restricted object
    @param field_name: The field name (using display_name)
    @param roles: An array with all the roles without permission for watching this field
    """
    if not aux.is_privatizable(obj, field_name):
        return False
    try:
        obj_type= ContentType.objects.get_for_model(obj)
        p=Restricted_fields.objects.get(content_type__pk=obj_type.id, 
                                        object_id=obj.id,
                                        field_name=field_name)
    except:
        p=Restricted_fields(element=obj, field_name=field_name)
        p.save()
    restrict_all(obj, roles)
    for role in roles:
        p.not_allowed_roles.add(role)
        
def restrict_undo(obj, field_name, roles):
    """
    Deletes the roles from the not allowed roles 
    
    @param obj: The object
    @param field_name: The field name (using display_name)
    @param roles: An array with all the roles that will be deleted from not allowed roles
    """
    if not aux.is_privatizable(obj, field_name):
        return False
    try:
        obj_type= ContentType.objects.get_for_model(obj)
        p=Restricted_fields.objects.get(content_type__pk=obj_type.id, 
                                     object_id=obj.id,
                                     field_name=field_name)
    except:
        return
    for role in roles:
        p.not_allowed_roles.remove(role)

def restrict_undo_all_fields(obj, roles):
    """
    Deletes the roles from the not allowed roles 
    
    @param obj: The object
    @param roles: An array with all the roles that will be deleted from not allowed roles
    """
    if not aux.is_privatizable(obj):
        return False
    try:
        obj_type= ContentType.objects.get_for_model(obj)
        fields=Restricted_fields.objects.filter(content_type__pk=obj_type.id, 
                                                object_id=obj.id)
        for field in fields:
            for role in roles:
                field.not_allowed_roles.remove(role)
    except:
        pass
        
def allow_all(obj, roles, strict=False):
    """
    Allows the access to the indicated object to the roles
    
    @param obj: The object
    @param roles: An array with all the roles with permission for watching this object
    @param strict: If the 
    
    @return: False if an error occurred
    """
    if not aux.is_privatizable(obj):
        return False
    try:
        obj_type= ContentType.objects.get_for_model(obj)
        p=Allowed_objects.objects.get(content_type__pk=obj_type.id, 
                                      object_id=obj.id)
    except:
        p=Allowed_objects(element=obj)
        p.save()
    for role in roles:
        if role.combo:
            to_delete = p.allowed_roles.filter(combo=role.combo)
            for r in to_delete:
                p.allowed_roles.remove(r)
        p.allowed_roles.add(role)
        
def allow_all_undo(obj, roles):
    """
    Deletes the roles permission for accessing to the indicated object
    
    @param obj: The object
    @param roles: An array with all the roles with permission for watching this object
    """
    if not aux.is_privatizable(obj):
        return False
    try:
        obj_type= ContentType.objects.get_for_model(obj)
        p=Allowed_objects.objects.get(content_type__pk=obj_type.id, 
                                      object_id=obj.id)
    except:
        return
    #Also remove this roles from the allowed fields of this objects.
    allow_undo_all_fields(obj, roles)
    for role in roles:
        p.allowed_roles.remove(role)
        
        
def restrict_all(obj, roles):
    """
    Restricts the access to the indicated object to the roles
    
    @param obj: The restricted object
    @param roles: An array with all the roles without permission for watching this object
    """
    if not aux.is_privatizable(obj):
        return False
    try:
        obj_type= ContentType.objects.get_for_model(obj)
        p=Restricted_objects.objects.get(content_type__pk=obj_type.id, 
                                                        object_id=obj.id)
    except:
        p=Restricted_objects(element=obj)
        p.save()
    for role in roles:
        p.not_allowed_roles.add(role)
        
def restrict_all_undo(obj, roles):
    """
    Deletes the roles restrictions for accessing to the object
    
    @param obj: The object
    @param roles: An array with all the roles that will be remove from the restriction
    """
    if not aux.is_privatizable(obj):
        return False
    try:
        obj_type= ContentType.objects.get_for_model(obj)
        p=Restricted_objects.objects.get(content_type__pk=obj_type.id, 
                                                        object_id=obj.id)
    except:
        return
    #Also remove this roles from the restricted fields of this objects.
    restrict_undo_all_fields(obj, roles)
    for role in roles:
        p.not_allowed_roles.remove(role)
        
def reset_privacy(obj):
    """
    Deletes all the privacy restrictions or permissions
    
    @param obj: the object
    """
    if not aux.is_privatizable(obj):
        return False
    try:
        obj_type= ContentType.objects.get_for_model(obj)
    except:
        return
    try:
        perm = Restricted_objects.objects.filter(content_type__pk=obj_type.id, 
                                                 object_id=obj.id)
        for p in perm:
            p.delete()
    except:
        return
    try:
        perm = Restricted_fields.objects.filter(content_type__pk=obj_type.id, 
                                                object_id=obj.id)
        for p in perm:
            p.delete()
    except:
        return
    try:
        perm = Allowed_objects.objects.filter(content_type__pk=obj_type.id, 
                                              object_id=obj.id)
        for p in perm:
            p.delete()
    except:
        return
    try:
        perm = Allowed_fields.objects.filter(content_type__pk=obj_type.id, 
                                             object_id=obj.id)
        for p in perm:
            p.delete()
    except:
        return
    
    
def create_role (name, objts=[], functions=[]):
    """
    Creates a role using the listed objects and functions
    
    @param name: The role name
    @param objts: The objects in this group
    @param functions: the functions per obtain a QuerySet of allowed objects
                      the param of this function will always be the restricted object id,
                      the requester object and a dictionary with more parameters

    @return: The role
    """
    role=Role(name=name)
    role.save()
    return add_to_role(name, objts, functions)

def add_to_role_or_create(name, objts=[], functions=[]):
    """
    Adds the objects and functions to the role if it exists, if not, 
    creates the new role using the objects and functions
    
    @param name: The role name
    @param objts: The objects in this group
    @param functions: the functions per obtain a QuerySet of allowed objects
                      the param of this function will always be the restricted object id
                      the requester object and a dictionary with more parameters

    @return: The role
    """
    try:
        return add_to_role(name, objts, functions)
    except:
        return create_role(name, objts, functions)

def add_to_role(name, objts=[], functions=[]):
    """
    Adds objects and functions to the role
    
    @param name: The name of the role
    @param objts: The objects that will be added to the role
    @param functions: The functions that will be added to the role
    
    @return: The role
    """
    role=get_role(name)
    for obj in objts:
        #Create Character objects for each one and add it to the role
        obj_type= ContentType.objects.get_for_model(obj)
        try:
            character = Character.objects.get(content_type__pk=obj_type.id, 
                                                        object_id=obj.id)
        except:
            character = Character(character = obj)
            character.save()
        role.characters.add(character)
    for function in functions:
        try:
            func, created=Function.objects.get_or_create(func=pickle.dumps(function["function"]), params=function["params"])            
            role.functions.add(func)
        except:
            func, created=Function.objects.get_or_create(func=pickle.dumps(function), params="")
            role.functions.add(func)
            pass
    role.save()
    return role

def delete_from_role(name, objts=[], functions=[]):
    """
    Deletes the objects and the functions from the selected role
    
    @param name: The role name
    @param objts: The objects that will be deleted from the role
    @param functions: The functions that will be deleted from the role
    
    @return: The role
    """
    role=get_role(name)
    for obj in objts:
        #Create Character objects for each one and add it to the role
        obj_type= ContentType.objects.get_for_model(obj)
        try:
            character = Character.objects.get(content_type__pk=obj_type.id, 
                                                        object_id=obj.id)
            role.characters.delete(character)
        except:
            pass
    for function in functions:
        try:
            func= Functions.objects.get(func=pickle.dumps(function["function"]), params=function["params"])
            role.functions.delete(func)
        except:
            try:
                func= Functions.objects.get(func=pickle.dumps(function), params="")
                role.functions.delete(func)
            except:
                pass
    role.save()
    return role

def delete_role (role_name):
    """
    Deletes the role whose name is role_name
    
    @param role_name: The name of the role that will be deleted
    """
    role= get_role(role_name)
    role.delete()

def get_role(name):
    """
    Returns a role if exists otherwise it return an exceptions.AttributeError
     exception
    
    @param name: The role name
    
    @return: The role
    """
    return Role.objects.get(name=name)

def get_all_roles_names():
    """
    Returns all the roles names
    
    @return: All the roles names
    """
    return Role.objects.values_list("name", flat=True)