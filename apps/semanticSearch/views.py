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
#    Author : Jose Gato Luis <jgato __at__ libresoft __dot__ es>
#


from SemanticManager import SemanticManager
from Relations.WordRelation import *

from social.core import api
from social.rest.utils import error

from xml.dom import minidom
from xml.dom.minidom import Document, parseString

from django.http import HttpResponse
from format.utils import  getResponseFormat, generateResponse

from compareNodes import CompareNodes
from utils import *


semanticManager = SemanticManager()
semanticManager.configure()

def semanticSearch(request):
    pass


    
def _checkSocialObjects(word, objects, fields):

    resume = []
    
    for object in objects:
        for field in fields:
            result = compareWordParagraph(word, object[field], object, semanticManager) 
            
            if result is not None:
                resume.append(result)
    
    return resume
    
def _returnPhotos():
    return api.photo.get_all()

def _checkPhotos(word):
    
    photos = _returnPhotos()
    fields = fieldsByType ("photo")
    resume = _checkSocialObjects (word, photos, fields)
    
    return resume

def _returnNotes():
    return api.note.get_all()

def _checkNotes(word):
    
    notes = _returnNotes()
    fields = fieldsByType ("note")
    resume = _checkSocialObjects (word, notes, fields)
    
    return resume
  
    
##
#
# Search semantic relations between a specified word and the different
# social nodes
#
# @param request: word: the word to search in the social nodes
#                 sense: the sense of the word
#                 type: noun or adjective 
# @return: returns a list of similar nodes respect to 'word'
##
def socialSearchSemantic(request):
   
    format = getResponseFormat (request)

    if "word" in request.GET:
        word = request.GET["word"]
    else:
        return error(format, "The request needs a word to compare (only English language supported ")

    if "sense" in request.GET:
        sense = request.GET["sense"]
    else:
        sense = 1  # default sense value
    
    semanticManager.setLema(word)
    semanticManager.setSense(1)
    semanticWord1 = semanticManager.start()

    if semanticWord1 is not None:
        checkPhotos = "false"
        checkNotes = "false"
        checkDefault = True
            
        if "checkPhotos" in request.GET:
            checkPhotos = request.GET["checkPhotos"].lower()
            checkDefault = False
        
        
        if "checkNotes" in request.GET:
            checkNotes = request.GET["checkNotes"].lower()
            checkDefault = False
        
        
        notes = []
        photos = []

        if checkPhotos == "true" or checkDefault == True:
            photos = _checkPhotos(word)
            
        if checkNotes == "true" or checkDefault == True:
            notes = _checkNotes(word) 
       
        #nodes = orderSemanticResults (nodes)
        
        results = { 'note': notes, 'photo': photos }
        
        data = {"code"  : '200',
                "results": results }
                
    
        return generateResponse(format, data, "similarityNodes")
    
    else:
        return error(format, "The request needs a word to compare (only English language supported ")


##
#
# Returns how similars are two words, using the semantic manager module
#
# @param request: word1: word 1 to compare
#                 word2: word 2 to compare
#                 type: noun or adjective 
# @return: returns a similarity value
##
def similarityWords(request):
    
    format = getResponseFormat (request)
    
    if "word1" in request.GET:
	   word1 = request.GET["word1"]
    else:
        return error(format, "The request needs two words to compare (only English language supported ")
    

    if "word2" in request.GET:
        word2 = request.GET["word2"]
    else:
        return error(format, "The request needs two words to compare (only English language supported ")

    semanticManager.setLema(word1)
    semanticManager.setSense(1)
    semanticWord1 = semanticManager.start()


    semanticManager.setLema(word2)
    semanticManager.setSense(1)
    semanticWord2 = semanticManager.start()

    if semanticWord1 is not None and semanticWord2 is not None:
        result = semanticManager.compareSemanticWords(semanticWord1, semanticWord2)
        data = {"code"  : '200',
                "similarity" : result }
    
        return generateResponse(format, data, "similarityWords")
    else:
        return error(format, "The request needs a word to compare (only English language supported)")



def _createDistanceInfo(node1, node2, distance):
    
    return { "node1" : {
                                            "id" : node1["id"],
                                            "type" : node1["type"]                                        
                                            },
                                            
                                "node2" : {
                                            "id" : node2["id"],
                                            "type" : node2["type"]
                                        },
                                "distance" : distance
            }
##
#
# Only for testing, extract the distance between different social nodes
#
##
def compareSemanticNodes(request):
    
    format = getResponseFormat (request)
    compareNodes = CompareNodes(semanticManager)
    
    if "min" in request.GET:
        min = int (request.GET["min"])
    else:
        min = 50
    
    notes = _returnNotes()
    photos = _returnPhotos()
    
    result = []
    
    for node1 in notes:
        for node2 in photos:
            distance = compareNodes.compareNodes (node1, node2)
            
            if distance > min:
                result.append( _createDistanceInfo(node1, node2, distance))
    
#    for node1 in photos:
#        for node2 in photos:
#            distance = compareNodes.compareNodes (node1, node2)
#            
#            if distance > min:
#                result.append( _createDistanceInfo(node1, node2, distance))
#    
#    
#    for node1 in notes:
#        for node2 in notes:
#            distance = compareNodes.compareNodes (node1, node2)
#            
#            if distance > min:
#                result.append( _createDistanceInfo(node1, node2, distance))
              
    data = {"code"  : '200',
            "distances" : result }
    
    return generateResponse(format, data, "compareNodes")
    

def compareTwoSemanticNodes(request, node_id1, node_id2):

    format = getResponseFormat (request)
        
    if not request.user.is_authenticated():
        return error (format, "The user is not authenticated")
    
    compareNodes = CompareNodes(semanticManager)
        
    node1 = api.node.get_data(node_id1, request.user)   
    node2 = api.node.get_data(node_id2, request.user)

    
    if  node1 is not None and node2 is not None:
        distance = compareNodes.compareNodes (node1, node2)
        data = {"code"  : '200',
                "distance" : distance }
        return generateResponse(format, data, "distanceNodes")
    else:
        return error (format, "The two nodes should exist and they should have the right permissions ")
        
    
        
        