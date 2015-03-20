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

import sys
from social.core.models import Tag

class Label(object):
    
    @staticmethod
    def dist(elem, elem2=None, centroid=None):
        """
        Returns the distance between elem and elem2 if provided or the cetroid. If
        none of them, the centroid or the elem2 are provided an error is returned
        
        @param elem: An element
        @param elem2: If the distance is calculated between two elements, this 
                    is the second elements
        @param centroid: If the distance is calculated between an element an a 
                    cluster centroid, this is the value of the centroid.
                    Typically the centroid is calculated with the function
                    centroid of the same class.
                    If the param elem is None, this param must be a tuple with to
                    centroid values, this is the way for comparing two centroids
        """
        if elem == None:
            if centroid != None:
                if len(centroid) == 2:
                    if centroid[0] == centroid[1]:
                        return 0
                    else:
                        return sys.maxint
                else:
                    raise ValueError("centroid value expected to be a tuple with two centroid values")
            else:
                raise ValueError("Expected centroid values")
        elif elem2 != None:
            #Distance 0 if the share a tag, maxint otherwise
            elem_tags=[t.tag for t in elem.tags.all()]
            elem2_tags=[t.tag for t in elem2.tags.all()]
            for tag in elem_tags:
                if tag in elem2_tags:
                    return 0
            return sys.maxint 
        elif centroid != None:
            #Here the centroid must be the label string
            elem_tags=[t.tag for t in elem.tags.all()]
            if centroid in elem_tags:
                return 0
            else:
                return sys.maxint
        else:
            #Raise exception
            raise ValueError("The elem2 or the centroid must be provided")
    
    @staticmethod
    def centroid(cluster):
        #The centroid will be the most repeated tag in the cluster
        tags=[]
        for e in cluster.elements:
            tags+=[t.tag for t in e.tags.all()]
        tags_set=list(set(tags))
        if len(tags) <= 0:
            return ""
        max=tags.count(tags[0])
        tag=tags[0]
        for t in tags_set:
            n=tags.count(t)
            if n > max:
                max=n
                tag=t
        return tag
    
    @staticmethod
    def cohesion(cluster, elem):
        elem_tags=[t.tag for t in elem.tags.all()]
        return cluster.centroid() in elem_tags 
        
    @staticmethod
    def group_data(cluster, algorithm):
        return {"name":"label-%s" % (cluster.centroid()) }
