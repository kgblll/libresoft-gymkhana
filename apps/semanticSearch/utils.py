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

from Relations.WordRelation import *

def compareWordParagraph(word, paragraph, socialObject, semanticManager):
    
    
    
    if paragraph != None and paragraph != "":
        wordsCompared = semanticManager.compareWordParagraph(word, paragraph, SemanticWordItem.TYPENOUN, 1)
        result = semanticManager.analyzeWordComparedSimple(wordsCompared)
        
        if result:
          
            betterValue = semanticManager.betterValueWordCompared(wordsCompared)
            resume = {'result': betterValue, 
                            'info':   (socialObject['type'], socialObject['id']),
                            'data':   socialObject 
                            }
            return resume
    return None

def compareParagraphs(paragraph1, paragraph2, socialObject1, socialObject2, semanticManager):
    
    
    if paragraph1 != None and paragraph1 != "" and paragraph2!= None and paragraph2 != "":
        wordsCompared = semanticManager.compareParagraphs(paragraph1, paragraph2)
        result = semanticManager.analyzeWordComparedSimple(wordsCompared)
        
        if result:
            betterValue = semanticManager.betterValueWordCompared(wordsCompared)
            resume = {'result': betterValue, 
                            'info1':   (socialObject1['type'], socialObject1['id']),
                            'info2':   (socialObject2['type'], socialObject2['id']),
                            'data1':   socialObject1,
                            'data2':   socialObject2, 
                            }
            return resume
    
    return None

def orderSemanticResults(resume):
    
    resumeOrdered = []
    while len (resume) > 0:
        maxInfo = 0
        index = 0
        i = 0
        for info in resume:
            result = info['result']
            if result[0][2] > maxInfo :
                maxInfo = result[0][2]
                index = i
            i = i + 1
     
        resumeOrdered.append (resume[index])
        del resume[index]
    
    return resumeOrdered   

def fieldsByType(type ):
        
    fields = []
        
    if type == "photo":
        fields = ["name", "description"]
    elif type == "note":
        fields = ["title", "text"]
        
    return fields
    