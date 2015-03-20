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
from datetime import datetime

from social.core.api_group import create_or_modify as create_or_modify_group
from social.core.api_group import join, unjoin
from social.core.models import Membership
from social.groupifier.models import DynGroup

class MasterAlgorithm(object):
    """
    This class defines the interface that all the algorithms must implement.
    """
    
    def __init__(self, name, data, functions, initial_groups, groupifier, extra_params,
                 min_dist, min_members):
        self.name = name
        self.data = data
        self.functions = functions
        self.initial_groups = initial_groups
        self.groupifier = groupifier
        self.extra_params = extra_params
        self.min_dist = min_dist
        self.min_members = min_members
        
        #Transform the initial groups in clusters
        self.clusters=[]
        #When there are no previously created groups sometimes an exception is
        #thrown, but I can't find why. Something goes wrong while making the
        #queries to the database
        if self.initial_groups.count() > 0:
            for group in self.initial_groups:
                cluster=Cluster(group=group, functions=self.functions, algorithm=self)
                self.clusters.append(cluster)
    
    def algorithm(self):
        raise NotImplementedError( "Sorry this method is not implemented, this class is just an interface, it must be overrided" )
    
    def run(self):
        
        self.algorithm()
        
        self.mix_clusters()    
        self.clean_clusters()
        for cluster in self.clusters:
            if cluster.group != None:
                data=self.functions.group_data(cluster, self)
                if "position" in data:
                    cluster.group.position=data["position"]
                self.__update_group(cluster.group, self.functions.group_data(cluster, self), cluster.elements)
            else:
                self.__create_group(self.functions.group_data(cluster, self), cluster.elements)
    
    def __create_group(self, group_data, elements):
        """
        Creates a new group (different from those in the init_groups)
        
        @param group_data: A dictionary with the group name and position 
            {"name": name, ["position": a django.contrib.gis.geos.Point object]}
        @param elements: An array (or something iterable) with all the elements
                in the group
        """
        
        group = DynGroup(name=group_data["name"], 
                         position=group_data.setdefault("position",
                                                        Point(0.0, 0.0, srid=4326)), 
                         groupifier=self.groupifier)
        group.save()
        for elem in elements:
            join(group.id, elem.id)
            
    def __update_group(self, group, group_data ,elements):
        """
        Changes the members of the group indicated
        
        @param group:  The original group that will be update
        @param elements: The new elements of the group 
        """
        if "position" in group_data:
            group.position = group_data["position"]
            group.pos_time = datetime.now()
        if "name" in group_data:
            group.name = group_data["name"]
        group.save()
        old_elements=[m.node1 for m in Membership.objects.filter(node2=group)]
        
        #First, add new elements
        for new_elem in elements:
            if new_elem not in old_elements:
                join(group.id, new_elem.id)
        #Then delete not present items
        for old in old_elements:
            if old not in elements:
                print "Deleting"
                unjoin(group.id, old.id)
                
    def clean_clusters(self):
        """
        Checks if all the elements in the clusters are close enough, and the cluster 
        have a minimum quantity of elements
        """
        to_delete=[]
        for cluster in self.clusters:
            cluster.check_cohesion()
            if len(cluster.elements) < self.min_members:
                to_delete.append(cluster)
        for cluster in to_delete:
            if cluster.group != None:
                cluster.group.delete()
            self.clusters.remove(cluster)
    
    def mix_clusters(self):
        """
        Checks if some clusters can be put together
        """
        to_delete=[]
        for i in range(len(self.clusters)):
            cluster=self.clusters[i]
            if cluster not in to_delete:
                for j in range(i+1, len(self.clusters)):
                    cluster2=self.clusters[j]
                    if cluster2 not in to_delete and cluster!=cluster2:
                        if self.functions.dist(None,
                              centroid=(cluster.centroid(), cluster2.centroid())) <= self.min_dist:
                            cluster.mix_with(cluster2)
                            to_delete.append(cluster2)
        for cluster in to_delete:
            self.clusters.remove(cluster)

class Cluster:
    """
    Represents a cluster, during the execution of the algorithm
    """
    
    def __init__(self, functions, algorithm, group=None):
        self.group=group
        self.functions=functions
        self.algorithm=algorithm
        self.__centroid=None
        if group:
            self.elements=[e.node1 for e in Membership.objects.filter(node2=group)]
        else:
            self.elements=[]
    
    def __str__(self):
        return "Cluster: {group: %s, elements: %s}" % (self.group, self.elements)
    
    def add(self, elem):
        """
        This method must be used to add new elements, adding elements directly
        to the array could result on a bad centroid.
        """
        self.__centroid=None
        self.elements.append(elem)
        
    def add_many(self, elems):
        """
        This method adds more than one element at once.
        """
        self.__centroid=None
        self.elements.extend(elems)
        
    def pop(self, index):
        """
        This method must be used in order to delete elements from the cluster, 
        otherwise the centroid could be calculated wrongly.
        """
        self.__centroid=None
        return self.elements.pop(index)
    
    def remove(self, element):
        """
        This method must be used in order to remove elements instead of remove 
        them directly from self.elements array. 
        """
        self.__centroid=None
        return self.elements.remove(element)
        
    def centroid(self):
        """
        Calculates the cluster centroid
        """
        if self.__centroid == None:
            self.__centroid=self.functions.centroid(self)
        return self.__centroid

    def check_cohesion(self):
        """
        Checks if all the elements are close enough and good candidates for this
        cluster, deleting the elements that do not satisfy this requisites.
        """
        to_remove=[]
        for elem in self.elements:
            if not self.functions.cohesion(self, elem):
                #The element is not close enough
                to_remove.append(elem)
        for elem in to_remove:
            self.remove(elem)
            
    def mix_with(self, other):
        """
        Mixes the current cluster with the other cluster provided, including in the
        current cluster the data from other.
        """
        if self.group==None:
            self.group=other.group
        elif other.group!=None:
            other.group.delete()
        self.add_many(other.elements)
        
