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

from django.contrib.gis.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

import pickle

class Character(models.Model):
    """
    Represents a character that has interaction with the privacy objects.
    Basically is a reference to a generic object this class is needed because
    there is a many to many relation between a role and generic objects.
    """
    #Object reference
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    character = generic.GenericForeignKey('content_type', 'object_id')
    
    objects = models.GeoManager()
    
    class Meta:
        unique_together = (("content_type", "object_id"),)

class Function(models.Model):
    """
    Represents a function defined by a string that can be created with pickle, 
     the parameter of this functions will always be the restricted object.
    """
    func = models.TextField()
    
    params = models.TextField() #A "pickled" dictionary
    
    objects = models.GeoManager()
    
    class Meta:
        unique_together = (("func", "params"),)

class Role(models.Model):
    """
    Represents a role. It can be defined by a set of characters and/or
    by a set of functions that determine all the objects that match the role 
    """
    #Object reference
    name = models.SlugField(unique=True)
    characters = models.ManyToManyField(Character)
    functions = models.ManyToManyField(Function)
    combo = models.IntegerField(null=True)
    
    objects = models.GeoManager()
    
    def contains(self, object, requester):
        """
        @return: True if requester belongs to this role, False otherwise
        """
        req = ContentType.objects.get_for_model(requester)
        if self.characters.filter(content_type__pk=req.id, object_id=requester.id).count():
            return True
        #Second check if the requester is in included in the query of any function 
        for func in self.functions.all():
            f=pickle.loads(func.func.encode("ascii"))
            try:
                par=pickle.loads(func.params.encode("ascii"))
            except:
                par={}
            if requester in f(object, requester, par):
                return True
        return False
    
class Allowed_fields(models.Model):
    """
    This model stores the roles that can access to a field of an object.
    """
    #Object reference
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    element = generic.GenericForeignKey('content_type', 'object_id')
    
    #Reference to field
    field_name = models.CharField(max_length=50)
    
    allowed_roles = models.ManyToManyField(Role)
    
    objects = models.GeoManager()
    
    class Meta:
        unique_together = (("content_type", "object_id", "field_name"),)
    
class Allowed_objects(models.Model):
    """
    This model stores the roles that can access to an object
    """
    #Object reference
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    element = generic.GenericForeignKey('content_type', 'object_id')
    
    allowed_roles = models.ManyToManyField(Role)
    
    objects = models.GeoManager()
    
    class Meta:
        unique_together = (("content_type", "object_id"),)
    
class Restricted_fields(models.Model):
    """
    This models stores the role that can't access to a field of an object.
    """
    #Object reference
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    element = generic.GenericForeignKey('content_type', 'object_id')
    
    #Reference to field
    field_name = models.CharField(max_length=50)
    
    not_allowed_roles = models.ManyToManyField(Role)

    objects = models.GeoManager()
    
    class Meta:
        unique_together = (("content_type", "object_id", "field_name"),)
    
class Restricted_objects(models.Model):
    """
    This model stores the roles that can't access to an object
    """
    #Object reference
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    element = generic.GenericForeignKey('content_type', 'object_id')
    
    not_allowed_roles = models.ManyToManyField(Role)
    
    objects = models.GeoManager()
    
    class Meta:
        unique_together = (("content_type", "object_id"),)
