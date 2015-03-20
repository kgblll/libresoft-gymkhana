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

from django.contrib.gis.geos import Point
from django.contrib.gis.geos import MultiPoint
from social.core.utils import distance
import math
from datetime import datetime

class Geo(object):
    
    distances = None
    
    def dist(self, elem, elem2=None, centroid=None):
        """
        Returns the distance between elem and elem2 if provided or the cetroid. If
        none of them, the centroid or the elem2 are provided an error is returned
        
        @param elem: An element
        @param elem2: If the distance is calculated between two elements, this 
                    is the second elements
        @param centroid: If the distance is calculated between an element an a 
                    cluster centroid, this is the value of the centroid.
                    Typically the centroid is calculated with the function
                    whith the same name, ex: label_dist will receive the centroid
                    calculated by label_centroid.
                    If the param elem is None, this param must be a tuple with to
                    centroid values, this is the way for comparing two centroids
        """
        if elem == None:
            if centroid != None:
                if len(centroid) == 2:
                    return distance(centroid[0], centroid[1])
                    #return centroid[0].distance(centroid[1])
                else:
                    raise ValueError("centroid value expected to be a tuple with two centroid values")
            else:
                raise ValueError("Expected centroid values")
        elif elem2 != None:
            if self.distances:
                return self.distances[elem][elem2]
            else:
                return distance(elem.position, elem2.position)
            #return elem.position.distance(elem2.position)
        elif centroid != None:
            return distance(centroid, elem.position)
            #return centroid.distance(elem.position)
        else:
            #Raise exception
            raise ValueError("The elem2 or the centroid must be provided")
    
    @staticmethod
    def centroid(cluster):
        points=[e.position for e in cluster.elements]
        centroid= MultiPoint(points).centroid
        centroid.srid=4326
        return centroid
    
    def cohesion(self, cluster, elem, max_dist=1.2):
        n_elems = len(cluster.elements)
        #max_dist = min_dist * n_elems
        too_far = 0
        for e in cluster.elements:
            if self.dist(elem, elem2=e) > max_dist:
                too_far += 1
        if too_far > (n_elems/4):
            return False
        else:
            return True
        
        
    @staticmethod
    def group_data(cluster, algorithm):
        now = datetime.now()
        return {"name":"geo-(%s, %s)-(%s)" % (round(cluster.centroid().get_x(), 2), round(cluster.centroid().get_y(), 2), now.strftime("%H:%M")), "position": cluster.centroid() }
        

