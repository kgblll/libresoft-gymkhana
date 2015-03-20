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

from django.contrib.gis.geos import Point
from django.contrib.contenttypes.models import ContentType

from models import Group, Person, Membership, Social_node
from utils import get_person, check_group_dict, add_person_to_group, add_node_to_group

from social.privacy.exceptions import PermissionError

def create_or_modify(group, modify=True):
    """
    Receives the group data and adds it to the database, if the
    group is already created, modifies it.
    """
    from social.privacy2.models import Privacy
    try:
        group, message=check_group_dict(group)
        if group == None :
            return False, message
        try:
            point = Point(float(group["longitude"]), float(group["latitude"]), srid=4326)
        except:
            return False, "Bad latitude and/or longitude value/s"
        g = None
        try:
            g = Group.objects.get(name=group['groupname'])
            if modify:
                g.position = point
                g.radius = group["radius"]
                g.altitude = group["altitude"]
            else:
                return False, "The group already exists"
        except:
            g = Group(name=group["groupname"], position=point, radius=group["radius"], altitude=group["altitude"])
        g.save()
        privacy = Privacy(node=g)
        privacy.save()
        
        return True, g.id
    except:
        return False, "Unknown error"

def get_all(viewer=None):
    """
    Returns all the groups in the database
    """
    try:
        v=get_person(viewer)
        groups = []
        groups_obj = Group.objects.all()
        for group in groups_obj:
            try:
                groups += [group.get_dictionary(v)]
            except PermissionError:
                pass
        return groups
    except:
        return []

def get_data(gid, viewer=None):
    """
    Returns the data for the group
    """
    v=get_person(viewer)
    try:
        g = Group.objects.get(pk=gid)
        return g.get_dictionary(v)
    except:
        return None

def delete(gid):
    """
    Deletes the group indicated
    """
    try:
        g = Group.objects.get(pk=gid)
        g.delete()
        return True, "No error"
    except:
        return False, "This group doesn't exist"

def join(group, node):
    """
    Joins the node to the group
    """
    try:
        g = Group.objects.get(pk=group)
        try:
            n = Social_node.objects.get(pk=node)
            add_node_to_group(n, g)
            return True, "No error"
        except:
            return False, "The user doesn't exist"
    except:
        return False, "The group doesn't exist"

def unjoin (group, person):
    """
    Deletes the person from the group
    """
    try:
        g = Group.objects.get(pk=group)
        try:
            n = Social_node.objects.get(pk=person)
            try:
                m = Membership.objects.get_relation(node1=n, node2=g)
                m.delete()
                return True, "No error"
            except:
                return False, "This user doesn't belong to this group"
        except:
            return False, "The user doesn't exist"
    except:
        return False, "The group doesn't exist"

def unjoin_all (group):
    """
    Deletes all the people from the group
    """
    try:
        g = Group.objects.get(pk=group)
        try:
            elems = Membership.objects.filter(node2=g)
            for e in elem:
                e.delete()
            return True, "No error"
        except:
            return False, "Error while deleting members from the group"
    except:
        return False, "The group doesn't exist"
    
def get_group_elements (group, viewer=None):
    """
    Returns a dictionary with a list of elements for each type
    """
    v=get_person(viewer)
    try:
        g = Group.objects.get(pk=group)
    except:
        return {}
    elems = Membership.objects.filter(node2=g)
    ret_data={}
    
    for elem in elems:
        type=elem.node1.type
        try:
            dict = elem.node1.get_node().get_dictionary(v)
            ret_data.setdefault(type,[])
            ret_data[type].append(dict)
        except:
            pass
    return ret_data

def get_for_user(viewer=None):
    """
    Returns all the user groups
    """
    try:
        v=get_person(viewer)
        groups = []
        groups_obj = Membership.objects.get_groups_for(v).distance(v.position).order_by("distance")
        
        for group in groups_obj:
            try:
                node = group.get_node()
                groups += [group.get_node().get_dictionary(v)]
            except PermissionError:
                pass
        return groups
    except:
        return []
