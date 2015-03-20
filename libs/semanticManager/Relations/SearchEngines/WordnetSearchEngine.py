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
from nltk.corpus import wordnet as wn
import nltk
import sys

class WordnetSearchEngine (GenericSearchEngine):

    def __init__ (self):
        self.corpus = None
        pass
    
    def __loadCorpus(self):
        if self.corpus != None:
            nltk.data.path.append (self.corpus)
        else:
            print "Error, no wordnet corpus specified."
            
    def configure(self, corpus):
        self.corpus = corpus
        self.__loadCorpus()
        print "corpus loaded..."
        pass
    
    def synset(self, lema, sense = 1, type = None):
        if type == None or type == "noun" :
            type = wn.NOUN 
        elif type == "verb":
            type = wn.VERB
        else:
            type = wn.NOUN
             
        wordSynsets = wn.synsets(lema, type) 
        
        if len(wordSynsets) >= sense:
            return wordSynsets[sense - 1 ]
        else:
            return None
        
    def synonyms(self, synset ):
        # Semantic relation
        return synset.lemma_names    
    
    def __splitSynsets(self, synsets):
       
        listTriplets = []
        

        for synset in synsets:
            triplet = ["", "", ""]
            
            info = synset.name.split('.')
            n = len(info)     
            triplet[0] = info[0]   
            for i in range(0, n-3):
                triplet[0] = triplet[0] + info[i + 1]
                
            triplet[1] = info[n-2]
            triplet[2] = int(info[n-1])
            listTriplets.append(triplet)
       
        return listTriplets

    def hyponyms(self, synset):
        # Semantic relation
        
        hyponyms = synset.hyponyms()
        return self.__splitSynsets(hyponyms)
               
    def derivated(self, synset):
        # Lexical relation
        # A synset is composed by several lemmas 
        # (The lexical entry for a single morphological form of a
        # sense-disambiguated word.)
        # Create a Lemma from a "<word>.<pos>.<number>.<lemma>"
        # Note that <word> and <lemma> can be different, e.g. the Synset
        # 'salt.n.03' has the Lemmas 'salt.n.03.salt', 'salt.n.03.saltiness' and
        # 'salt.n.03.salinity'.
        #
        # Manually with only a synset is not possible to disambiguated a word
        # so the first lemma will be used

        return synset.lemmas[0].derivationally_related_forms()
    
    def partMeronyms(self, synset):
        
        partMeronyms = synset.part_meronyms()
        return self.__splitSynsets(partMeronyms)
    
    def partHolonyms(self, synset):
        
        partMeronyms = synset.part_holonyms()
        return self.__splitSynsets(partMeronyms)
        
    def pathSimilarity(self, synsetWord1, synsetWord2):
        return wn.path_similarity ( synsetWord1, synsetWord2 )

    def lchSimilarity(self, synsetWord1, synsetWord2):
        return wn.lch_similarity ( synsetWord1, synsetWord2 )
    
    def wupSimilarity(self, synsetWord1, semanticWord2):
        try:
            result = wn.wup_similarity(synsetWord1, semanticWord2)
            return result
        except: 
            print "Unexpected error:", sys.exc_info()[0]
            return 0
    
    

        
    

        
        
        
        
        
        
        
    
    
