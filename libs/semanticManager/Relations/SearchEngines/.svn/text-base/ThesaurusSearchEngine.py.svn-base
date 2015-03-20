#!/usr/bin/env python

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
#

from GenericSearchEngine import *
from Relations.Items.SemanticWordItem import *

from xml.dom import minidom
from xml.dom.minidom import Document, parseString

import httplib2

class ThesaurusSearchEngine (GenericSearchEngine):
    APIKEY = "33d681d63f49750e7afafba31788bec3"
    URLSERVER = "http://words.bighugelabs.com/api/2/"
    
    def __init__ (self):
        
        self.http = httplib2.Http(".cache")
        
        pass
           
    def configure(self, corpus):
        
        pass
  
        
    def __getRequest(self, lema):
        
        
        resp, content = self.http.request( self.URLSERVER + self.APIKEY + "/" + lema + "/xml", 
                                   "GET")
        return (resp, content)
        
        pass
    
    def __extractSynonymousXML(self, xml, type):
        
         conf = minidom.parseString(xml)
         wordsXML = conf.getElementsByTagName("w");
         
         synonymousList = []
         for word in wordsXML:
             if word.getAttribute("r") == "syn" and word.getAttribute("p") == type:
                 synonymousList.append( word.firstChild.data) 
         
         return synonymousList
         
    
    def synonyms(self, lema, type = None):

        (resp, content) = self.__getRequest(lema)
        
        synonymousList = []
        status = resp['status']
         
        if status ==  "200" :
            if (type == None):
                type = SemanticWordItem.TYPENOUN
            synonymousList = self.__extractSynonymousXML(content, type)
            pass
        else:
            print "ThesaurusSearchEngine: connecting to the server : ", status

        return synonymousList

 
    

        
    

        
        
        
        
        
        
        
    
    