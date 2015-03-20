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

from social.groupifier.algorithms import MasterAlgorithm, Cluster
import random


class KmeansAlgorithm(MasterAlgorithm):
    
    def algorithm(self):
        self.calculate_distances_array()
        self.create_new_clusters()
        to_remove = []
        
        clusters_changed=True
        while clusters_changed:
            clusters_changed=False
            for cluster in self.clusters:
                for elem in cluster.elements:
                    #Look for a new group closest than actual
                    actual_dist = self.functions.dist(elem,
                                                  centroid=cluster.centroid())
                    actual_cluster = cluster
                    for c in self.clusters:
                        new_dist=self.functions.dist(elem,
                                                    centroid=c.centroid())
                        if new_dist<actual_dist:
                            actual_dist=new_dist
                            actual_cluster=c
                    if actual_cluster != cluster:
                        cluster.remove(elem)
                        if len(cluster.elements) == 0:
                           try:
                              self.clusters.remove(cluster)
                              if cluster.group:
                                  cluster.group.delete()
                           except:
                              pass
                        actual_cluster.add(elem)
                        clusters_changed=True

    def create_new_clusters(self):
        """
        Creates "num_cluster" new clusters using the unclustered elements
        """
        #First check for ungrouped elements
        ungrouped=[]
        for e in self.data:
            present=False
            for clus in self.clusters:
                if e in clus.elements:
                    present=True
                    break
            if not present:
                #Try to assign the element to near clusters
                group = None
                min_dist = self.min_dist
                for cluster in self.clusters:
                    dist = self.functions.dist(e,
                                               centroid=cluster.centroid())
                    if dist < min_dist:
                        group = cluster
                        min_dist = dist
                if group != None:
                    group.add(e)
                else:
                    ungrouped.append(e)
        #Put all the ungrouped elements in groups
        num_cluster = len(ungrouped)/4
        new_clusters=[]
        try:
            n_elem=float(len(ungrouped))/num_cluster
        except ZeroDivisionError:
            return
        random.shuffle(ungrouped)
        for i in range(num_cluster):
            c=Cluster(functions=self.functions, algorithm=self)
            init=int(i*n_elem)
            end=int((i+1)*n_elem)
            c.add_many(ungrouped[init:end])
            #Group params
            self.clusters.append(c)
            
    def calculate_distances_array(self):
        """
        Creates an array with the distances between all the elements.
        """
        self.distances={}
        for e in self.data:
            self.distances[e] = {}
        for i in range(len(self.data)):
            elem1 = self.data[i]
            for j in range(i, len(self.data)):
                elem2 = self.data[j]
                dist = self.functions.dist(elem=elem1, elem2=elem2)
                self.distances[elem1][elem2] = dist
                self.distances[elem2][elem1] = dist
        
        #Pass it to the functions class
        
        self.functions.distances = self.distances

        print self.functions 
