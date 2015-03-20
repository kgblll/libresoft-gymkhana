# -*- coding: utf-8 -*-
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

from social.core.models import Person, Note, Photo, Social_node, Sound

from social.privacy.utils import get_role, allow, allow_all, restrict, restrict_all
from social.privacy.utils import allow_undo, allow_all_undo, restrict_undo, restrict_all_undo
from social.privacy.utils import add_to_role_or_create
from social.privacy2.utils import get_all_roles_names, get_perm_names

def get_all_roles():
    """
    Returns all the roles, except the person roles
    """
    roles=get_all_roles_names()
    final_roles=[]
    for role in roles:
        if role.find("person-")!=0:
            final_roles.append(role)
    return final_roles

def get_permissions_names():
    return get_perm_names()
    
def privacy_change(user_id, node_id, perm=None, field = None):
    try:
        user = Person.objects.get(id = user_id)
    except:
        return False, "User doesn't exist"
    try:
        n = Social_node.objects.get(id = node_id)
    except:
        return False, "Node does't exist"
    node = n.get_node()
    if node.get_owner().id != user.id:
        return False, "This node is not yours"
    
    if perm != None:
        if field != None:
            if not node.set_perm_field(field,perm):
                return False, "Error changing field: %s permissions" % (field)
        else:
            if not node.set_perm(perm):
                return False, "Error changing permissions"
    
    return True, "No error"

def get_permissions(user_id, node_id):
    try:
        user = Person.objects.get(id = user_id)
    except:
        return False, "User doesn't exist"
    try:
        n = Social_node.objects.get(id=node_id)
    except:
        return False, "Node doesn't exist"
    node = n.get_node()
    if node.get_owner().id != user.id:
        return False, "This node is not yours"
    
    return True, node.get_privacy()

#def get_user_permissions(user_id):
    #"""
    #Returns the permissions/restrictions for a user
    #"""
    #try:
        #p = Person.objects.get(pk=user_id)
        #perm = p.get_privacy()
        #return True, perm
    #except:
        #return False, "The user doesn't exist"
    
#def allow_access(user_id, field=None, roles=[], users=[], undo=False):
    #"""
    #Allows the roles and users access to the user object or the user field 
    #"""
    #try:
        #p=Person.objects.get(pk=user_id)
    #except:
        #return False, "The user doesn't exist"
    #try:
        #role_objs=[]
        #for role in roles:
            #try:
                #role_objs.append(get_role(role))
            #except:
                #return False, 'Role "%s" does not exist' % role
        #for r in role_objs:
            #if field:
                #if undo:
                    #p.allow_undo(field, [r])
                #else:
                    #p.allow(field, [r])
            #else:
                #if undo:
                    #p.allow_all_undo([r])
                #else:
                    #p.allow_all([r])
        #for user in users:
            #user_obj=Person.objects.get(pk=user)
            #name="person-%s" % user_obj.username
            #r=add_to_role_or_create(name, objts=[user_obj])
            #if field:
                #if undo:
                    #p.allow_undo(field, [r])
                #else:
                    #p.allow(field, [r])
            #else:
                #if undo:
                    #p.allow_all_undo([r])
                #else:
                    #p.allow_all([r])
        #return True, "No error"
    #except:
        #return False, "Unexpected error"

#def restrict_access(user_id, field=None, roles=[], users=[], undo=False):
    #"""
    #Restricts the roles and users access to the user object or the user field 
    #"""
    #try:
        #p=Person.objects.get(pk=user_id)
    #except:
        #return False, "The user doesn't exist"
    #try:
        #role_objs=[]
        #for role in roles:
            #try:
                #role_objs.append(get_role(role))
            #except:
                #return False, 'Role "%s" does not exist' % role
        #for r in role_objs:
            #r=get_role(role)
            #if field:
                #if undo:
                    #p.restrict_undo(field, [r])
                #else:
                    #p.restrict(field, [r])
            #else:
                #if undo:
                    #p.restrict_all_undo([r])
                #else:
                    #p.restrict_all([r])
        #for user in users:
            #user_obj=Person.objects.get(pk=user)
            #name="person-%s" % user_obj.username
            #r=add_to_role_or_create(name, objts=[user_obj])
            #if field:
                #if undo:
                    #p.restrict_undo(field, [r])
                #else:
                    #p.restrict(field, [r])
            #else:
                #if undo:
                    #p.restrict_all_undo([r])
                #else:
                    #p.restrict_all([r])
        #return True, "No error"
    #except:
        #return False, "Unexpected error"

#def get_note_permissions(note_id, viewer_id):
    #"""
    #Returns the permissions/restrictions for a note
    #"""
    #try:
        #p = Person.objects.get(pk=viewer_id)
    #except:
        #return False, "User doesn't exist"
    #try:
        #n = Note.objects.get(pk=note_id)
        #if p == n.uploader:
            #perm = n.get_privacy()
            #return True, perm
        #else:
            #return False, "This note is not yours"
    #except:
        #return False, "The note doesn't exist"
    
#def note_allow_access(user_id, note_id=None, roles=[], users=[], undo=False, field=None):
    #"""
    #Allows permission for view the note for the roles and users indicated. If 
    #note_id is None, all user notes permissions will be modified
    #"""
    #try:
        #p = Person.objects.get(pk=user_id)
    #except:
        #return False, "User doesn't exist"
    #if note_id:
        #try:
            #n = Note.objects.get(pk=note_id)
            #if p == n.uploader:
                #notes=[n]
            #else:
                #return False, "This note is not yours"
        #except:
            #return False, "The note doesn't exist"
    #else:
        #Change all user notes
        #notes=Note.objects.filter(uploader=p)
        #if not notes:
            #return False, "User doesn't have notes"
    #o_roles=[]
    #try:
        #for user in users:
            #user_obj=Person.objects.get(pk=user)
            #name="person-%s" % user_obj.username
            #r=add_to_role_or_create(name, objts=[user_obj])
            #o_roles.appen(r)
    #except:
        #return False, "One or more users do not exist"

    #for role in roles:
        #try:
            #r=get_role(role)
            #o_roles.append(r)
        #except:
            #return False, 'Role "%s" does not exist' % role

    #for n in notes:
        #for r in o_roles:
            #if field:
                #if undo:
                    #n.allow_undo(field, [r])
                #else:
                    #n.allow(field, [r])
            #else:
                #if undo:
                    #n.allow_all_undo([r])
                #else:
                    #n.allow_all([r])
    #return True, "Permission updated correctly"

#def note_restrict_access(user_id, note_id=None, roles=[], users=[], undo=False, field=None):
    #"""
    #Restrict permission for view the note for the roles and users indicated. If 
    #note_id is None, all user notes permissions will be modified
    #"""
    #try:
        #p = Person.objects.get(pk=user_id)
    #except:
        #return False, "User doesn't exist"
    #if note_id:
        #try:
            #n = Note.objects.get(pk=note_id)
            #if p == n.uploader:
                #notes=[n]
            #else:
                #return False, "This note is not yours"
        #except:
            #return False, "The note doesn't exist"
    #else:
        #Change all user notes
        #notes=Note.objects.filter(uploader=p)
        #if not notes:
            #return False, "User doesn't have notes"
        
    #o_roles=[]
    #try:
        #for user in users:
            #user_obj=Person.objects.get(pk=user)
            #name="person-%s" % user_obj.username
            #r=add_to_role_or_create(name, objts=[user_obj])
            #o_roles.appen(r)
    #except:
        #return False, "One or more users do not exist"

    #for role in roles:
        #try:
            #r=get_role(role)
            #o_roles.append(r)
        #except:
            #return False, 'Role "%s" does not exist' % role

    #for n in notes:
        #for r in o_roles:
            #if field:
                #if undo:
                    #n.restrict_undo(field, [r])
                #else:
                    #n.restrict(field, [r])
            #else:
                #if undo:
                    #n.restrict_all_undo([r])
                #else:
                    #n.restrict_all([r])
    #return True, "Permission updated correctly"

#def get_photo_permissions(photo_id, viewer_id):
    #"""
    #Returns the permissions/restrictions for a photo
    #"""
    #try:
        #p = Person.objects.get(pk=viewer_id)
    #except:
        #return False, "User doesn't exist"
    #try:
        #photo = Photo.objects.get(pk=photo_id)
        #if p == photo.uploader:
            #perm = photo.get_privacy()
            #return True, perm
        #else:
            #return False, "This photo is not yours"
    #except:
        #return False, "The photo doesn't exist"
    
#def photo_allow_access(user_id, photo_id=None, roles=[], users=[], undo=False, field=None):
    #"""
    #Allows permission for view the photo for the roles and users indicated. If 
    #photo_id is None, all user photos permissions will be modified
    #"""
    #try:
        #p = Person.objects.get(pk=user_id)
    #except:
        #return False, "User doesn't exist"
    #if photo_id:
        #try:
            #photo = Photo.objects.get(pk=photo_id)
            #if p == photo.uploader:
                #photos=[photo]
            #else:
                #return False, "This photo is not yours"
        #except:
            #return False, "The photo doesn't exist"
    #else:
        #Change all user photos
        #photos=Photo.objects.filter(uploader=p)
        #if not photos:
            #return False, "User doesn't have photos"
    #o_roles=[]
    #try:
        #for user in users:
            #user_obj=Person.objects.get(pk=user)
            #name="person-%s" % user_obj.username
            #r=add_to_role_or_create(name, objts=[user_obj])
            #o_roles.appen(r)
    #except:
        #return False, "One or more users do not exist"

    #for role in roles:
        #try:
            #r=get_role(role)
            #o_roles.append(r)
        #except:
            #return False, 'Role "%s" does not exist' % role

    #for p in photos:
        #for r in o_roles:
            #if field:
                #if undo:
                    #p.allow_undo(field, [r])
                #else:
                    #p.allow(field, [r])
            #else:
                #if undo:
                    #p.allow_all_undo([r])
                #else:
                    #p.allow_all([r])
    #return True, "Permission updated correctly"

#def photo_restrict_access(user_id, photo_id=None, roles=[], users=[], undo=False, field=None):
    #"""
    #Restrict permission for view the photo for the roles and users indicated. If 
    #photo_id is None, all user photos permissions will be modified
    #"""
    #try:
        #p = Person.objects.get(pk=user_id)
    #except:
        #return False, "User doesn't exist"
    #if photo_id:
        #try:
            #photo = Photo.objects.get(pk=photo_id)
            #if p == photo.uploader:
                #photos=[photo]
            #else:
                #return False, "This photo is not yours"
        #except:
            #return False, "The photo doesn't exist"
    #else:
        #Change all user photos
        #photos=Photo.objects.filter(uploader=p)
        #if not photos:
            #return False, "User doesn't have photos"
    #o_roles=[]
    #try:
        #for user in users:
            #user_obj=Person.objects.get(pk=user)
            #name="person-%s" % user_obj.username
            #r=add_to_role_or_create(name, objts=[user_obj])
            #o_roles.appen(r)
    #except:
        #return False, "One or more users do not exist"

    #for role in roles:
        #try:
            #r=get_role(role)
            #o_roles.append(r)
        #except:
            #return False, 'Role "%s" does not exist' % role

    #for p in photos:
        #for r in o_roles:
            #if field:
                #if undo:
                    #p.restrict_undo(field, [r])
                #else:
                    #p.restrict(field, [r])
            #else:
                #if undo:
                    #p.restrict_all_undo([r])
                #else:
                    #p.restrict_all([r])
    #return True, "Permission updated correctly"

#def get_sound_permissions(sound_id, viewer_id):
    #"""
    #Returns the permissions/restrictions for a sound
    #"""
    #try:
        #p = Person.objects.get(pk=viewer_id)
    #except:
        #return False, "User doesn't exist"
    #try:
        #sound = Sound.objects.get(pk=sound_id)
        #if p == sound.uploader:
            #perm = sound.get_privacy()
            #return True, perm
        #else:
            #return False, "This sound is not yours"
    #except:
        #return False, "The sound doesn't exist"

#def sound_restrict_access(user_id, sound_id=None, roles=[], users=[], undo=False, field=None):
    #"""
    #Restrict permission for view the sound for the roles and users indicated. If 
    #sound_id is None, all user sounds permissions will be modified
    #"""
    #try:
        #p = Person.objects.get(pk=user_id)
    #except:
        #return False, "User doesn't exist"
    #if sound_id:
        #try:
            #sound = Sound.objects.get(pk=sound_id)
            #if p == sound.uploader:
                #sounds=[sound]
            #else:
                #return False, "This sound is not yours"
        #except:
            #return False, "The sound doesn't exist"
    #else:
        #Change all user sounds
        #sounds=Sound.objects.filter(uploader=p)
        #if not sounds:
            #return False, "User doesn't have sounds"
    #o_roles=[]
    #try:
        #for user in users:
            #user_obj=Sound.objects.get(pk=user)
            #name="person-%s" % user_obj.username
            #r=add_to_role_or_create(name, objts=[user_obj])
            #o_roles.appen(r)
    #except:
        #return False, "One or more users do not exist"

    #for role in roles:
        #try:
            #r=get_role(role)
            #o_roles.append(r)
        #except:
            #return False, 'Role "%s" does not exist' % role

    #for s in sounds:
        #for r in o_roles:
            #if field:
                #if undo:
                    #s.restrict_undo(field, [r])
                #else:
                    #s.restrict(field, [r])
            #else:
                #if undo:
                    #s.restrict_all_undo([r])
                #else:
                    #s.restrict_all([r])
    #return True, "Permission updated correctly"

#def sound_allow_access(user_id, sound_id=None, roles=[], users=[], undo=False, field=None):
    #"""
    #Allows permission for view the sound for the roles and users indicated. If 
    #sound_id is None, all user sounds permissions will be modified
    #"""
    #try:
        #p = Person.objects.get(pk=user_id)
    #except:
        #return False, "User doesn't exist"
    #if sound_id:
        #try:
            #sound = Sound.objects.get(pk=sound_id)
            #if p == sound.uploader:
                #sounds=[sound]
            #else:
                #return False, "This sound is not yours"
        #except:
            #return False, "The sound doesn't exist"
    #else:
        #Change all user sounds
        #sounds=Sound.objects.filter(uploader=p)
        #if not sounds:
            #return False, "User doesn't have sounds"
    #o_roles=[]
    #try:
        #for user in users:
            #user_obj=Person.objects.get(pk=user)
            #name="person-%s" % user_obj.username
            #r=add_to_role_or_create(name, objts=[user_obj])
            #o_roles.appen(r)
    #except:
        #return False, "One or more users do not exist"

    #for role in roles:
        #try:
            #r=get_role(role)
            #o_roles.append(r)
        #except:
            #return False, 'Role "%s" does not exist' % role

    #for s in sounds:
        #for r in o_roles:
            #if field:
                #if undo:
                    #s.allow_undo(field, [r])
                #else:
                    #s.allow(field, [r])
            #else:
                #if undo:
                    #s.allow_all_undo([r])
                #else:
                    #s.allow_all([r])
    #return True, "Permission updated correctly"

#def node_allow_all(user_id, node_id, roles=[], users=[], undo=False):
    #"""
    #Allows access to all fields of the node with the given id to the roles and
    #users indicated.
    #"""
    #try:
        #p = Person.objects.get(pk=user_id)
    #except:
        #return False, "User doesn't exist"
    #try:
        #node = Social_node.objects.get(pk=node_id)
        #if p != node.get_owner():
            #return False, "This node is not yours"
    #except:
        #return False, "The node doesn't exist"
    #o_roles=[]
    #try:
        #for user in users:
            #user_obj=Person.objects.get(pk=user)
            #name="person-%s" % user_obj.username
            #r=add_to_role_or_create(name, objts=[user_obj])
            #o_roles.appen(r)
    #except:
        #return False, "One or more users do not exist"

    #for role in roles:
        #try:
            #r=get_role(role)
            #o_roles.append(r)
        #except:
            #return False, 'Role "%s" does not exist' % role

    #if undo:
        #node.allow_all_undo(o_roles, all_fields=True)
    #else:
        #node.allow_all(o_roles, all_fields=True)
    #return True, "Permission updated correctly"
    
#def reset_privacy(user_id, node_id):
    #"""
    #Resets the object privacy
    #"""
    #try:
        #p = Person.objects.get(pk=user_id)
    #except:
        #return False, "User doesn't exist"
    #try:
        #node = Social_node.objects.get(pk=node_id)
        #if p != node.get_owner():
            #return False, "This node is not yours"
        #node.reset_privacy()
    #except:
        #return False, "The node doesn't exist"
    #return True, "Permission updated correctly"
