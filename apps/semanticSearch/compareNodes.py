#  Copyright (C) 2009 GSyC/LibreSoft
# 
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see http://www.gnu.org/licenses/.
#
#  Author : Jose Gato Luis <jgato@libresoft.es>


from SemanticManager import SemanticManager
from utils import *

class CompareNodes:
    
    
    def __init__ (self, semanticManager = None):
        if semanticManager is not None:
            self.semanticManager = semanticManager
        else:
            self.semanticManager = SemanticManager()
            self.semanticManager.configure()
    
    
    ##
    #
    # Compare two social nodes (no matter the node type), returning a semantic
    # distance value
    #
    # @param node1: social node
    # @param node2: social node
    #
    # @return: returns a distance value
    ##
    def compareNodes( self, node1, node2,  ):
        
        type1 = node1["type"]
        fields1 = fieldsByType(type1)
        type2 = node2["type"]
        fields2 = fieldsByType(type2)
        
        resume = []
        for field1 in fields1:
            for field2 in fields2:
                p1 = node1[field1]
                p2 = node2[field2]
     
                result = compareParagraphs(p1, p2, node1, node2, self.semanticManager)
                if result is not None:
                    resume.append(result)
         
        distance = self._distanceNodes(resume)
        
        if distance == 0:
            distance = self.semanticManager.semanticManagarSimilarityMax
        else:
            distance = 1 / distance
        
        print "Result: node1: ", node1["id"], " (", node1["type"], ") against node: ", node2["id"], " (", node2["type"], ") distance: ", distance
        print "======================================================================================"
                
        return distance
    

    def _distanceNodes(self, fieldsAnalysis ):
        """
         Many Algorithms possibilities:
            The easiest way: return the highest value of all the fields combinations compared
        """
        
        distance = 0
        for analysis in fieldsAnalysis:
            analysisDistance = analysis['result'][2]
            
            if analysisDistance > distance:
                distance = analysisDistance
                
        return distance
    