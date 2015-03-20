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


import SemanticManagerSettings
from GenericRelation import *
from Items import SemanticWordItem
from SearchEngines.WordnetSearchEngine import *
from SearchEngines.ThesaurusSearchEngine import *
from Items.SemanticWordItem import *

class WordRelation (GenericRelation):

    def __init__ (self, engine = None):
        if engine == None:
            self.engine = WordnetSearchEngine()
            self.corpus_path = SemanticManagerSettings.CORPUSPATH
            self.engine.configure( self.corpus_path )
        else:
            self.engine = engine
        
        #self.thesaurus = ThesaurusSearchEngine()
        
        
        self.lema = None
        self.type = None
        self.sense = 1
        self.depthHyponyms = 1
        
    def setDepthHyponyms (self, depth):
        self.depthHyponyms = depth
        
    def setSense (self, sense):
        self.sense = sense
        
    def setLema (self, lema):
        self.lema = lema 
        
    def setType (self, type):
        self.type = type
        
    def generateHyponyms (self, word, synset, depth ):
        
        if depth == 0:
            return
        else:
            hyps = self.engine.hyponyms (synset)
            for hyp in hyps:
                #hyp[0] = hyp[0].replace("_", " ")
                if hyp[1] == "n":
                    type = SemanticWordItem.TYPENOUN
                elif hyp[1] == "v":
                    type = SemanticWordItem.TYPEVERB
                else:
                    type = None
                    
                wordItem = self.__createWordItem( hyp[0], hyp[2], type)

                if not wordItem is None:
                    
                    hypSynset = self.engine.synset( hyp[0], hyp[2], type)
                    if not hypSynset is None:
                        wordItem.setSynonyms( self.engine.synonyms( hypSynset))
                        wordItem.setDerivated( self.engine.derivated( hypSynset))
                        
                        word.setHyponyms (wordItem)
                           
                        self.generateHyponyms(wordItem, hypSynset, depth -1)
                    else: #FIXME: this should not happen
                        print "Error, this should not happen (no synset for ", hyp[0], hyp[2], type, ")"
        
    
    def generatePartMeronyms(self, word, synset):
        partMeronyms = self.engine.partMeronyms (synset)
        for partMeronym in partMeronyms:
                
                if partMeronym[1] == "n":
                    type = SemanticWordItem.TYPENOUN
                elif partMeronym[1] == "v":
                    type = SemanticWordItem.TYPEVERB
                else:
                    type = None
                    
                wordItem = self.__createWordItem( partMeronym[0], partMeronym[2], type)
                if not wordItem is None:
                    word.setPartMeronyms (wordItem)
        
    def generatePartHolonyms(self, word, synset):
        partHolonyms = self.engine.partHolonyms(synset)
        
        for partHolonym in partHolonyms:
                
                if partHolonym[1] == "n":
                    type = SemanticWordItem.TYPENOUN
                elif partHolonym[1] == "v":
                    type = SemanticWordItem.TYPEVERB
                else:
                    type = None
                    
                wordItem = self.__createWordItem( partHolonym[0], partHolonym[2], type)
                if not wordItem is None:
                    word.setPartHolonyms (wordItem)
           
    def __createWordItem(self, lema, sense = 1, type = None):
        wordItem = SemanticWordItem()
        wordItem.setLema (lema)
        wordItem.setSense (sense)
        wordItem.setType (type)
        
        return wordItem
        
    def start (self):
        synset = self.engine.synset( self.lema, self.sense, self.type)
        if (synset is not None):
            
            wordItem =  self.__createWordItem(self.lema, self.sense, self.type)
            
            if not wordItem is None:
                wordItem.setSynonyms( self.engine.synonyms( synset))
                #wordItem.appendSynonyms( self.thesaurus.synonyms( wordItem.getLema(), wordItem.getType()))
                wordItem.setDerivated( self.engine.derivated( synset))
                self.generateHyponyms( wordItem, synset, self.depthHyponyms)
                self.generatePartMeronyms( wordItem, synset)
                self.generatePartHolonyms( wordItem, synset)
                
            
            return wordItem
        else:
            return None
        
        










