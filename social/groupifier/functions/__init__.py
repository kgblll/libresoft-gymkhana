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

def Functions(object):
    """
    This is the superclass for all the defining functions classes.
    """
    
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
        raise NotImplementedError( "Sorry this method is not implemented, this class is just an interface, it must be overrided" )
    
    @staticmethod
    def centroid(cluster):
        raise NotImplementedError( "Sorry this method is not implemented, this class is just an interface, it must be overrided" )
    
    @staticmethod
    def cohesion(cluster, elem, cohesion_factor=1.2):
        raise NotImplementedError( "Sorry this method is not implemented, this class is just an interface, it must be overrided" )
    
    @staticmethod
    def group_data(cluster, algorithm):
        raise NotImplementedError( "Sorry this method is not implemented, this class is just an interface, it must be overrided" )
