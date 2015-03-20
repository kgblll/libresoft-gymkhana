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

from social.core.models import Group
from social.privacy.utils import get_fields
from social.core.utils import get_fields_for_groups

class Groupifier(models.Model):
    """
    This models stores in the database the groupifiers, what means the algorithms
    used to create new groups with the related data. 
    """
    
    name = models.CharField(max_length=80, unique=True)
    algorithm = models.TextField()                          #Pickled class
    data_set_model = models.TextField()                     #Pickled Model
    data_set_query = models.TextField()                     #Pickled Query
    functions = models.TextField()                          #Pickled Functions class child
    min_members = models.IntegerField()                     
    min_dist = models.FloatField()
    extra_params = models.TextField()                       #Pickled dictionary
    
    objects = models.GeoManager()
    

class DynGroup(Group):
    """
    This class is a group implementation with an extra attribute to indicate the 
    groupifier that created it 
    """
    
    groupifier = models.ForeignKey(Groupifier, related_name="groups")
    
    objects = models.GeoManager()
    
    def get_dictionary(self, viewer=None):
        """
        Returns the dyngroup data as a dictionary
        """
        dict = Group.get_dictionary(self, viewer)
        dict["groupifier"]=self.groupifier.name
        if viewer!=None:
            fields = get_fields(self, viewer)
            groups = get_fields(self, viewer)
            if groups==None:
                raise PermissionError("Element not allowed")
            fields= get_fields_for_groups(self, groups)
            if "groupifier" not in fields:
                dict.pop("groupifier")
        return dict
