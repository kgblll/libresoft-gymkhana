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


from GenericItem import *

class SemanticWordItem (GenericItem):
    """
    A class to store semantic information about a word,
        * sense and type are optional, but they will give contextual information to a word. Ex.:
          the word/lema bank could be different depending on
          the sense and the type (verb, noun)
          
        * Every semanticworditem needs a sense (0 by default) if this configuration
          is ignored (maybe you dont know which sense are you analysing), you could be
          loosing contextual information. Ex.: The word/lema 'dog' by default will have the
          next definition:
          '''a member of the genus Canis (probably descended from the common wolf) that has 
          been domesticated by man since prehistoric times'''
          But maybe, in the text that you are analysing the word dog means:
          '''informal term for a man'''
          Because it was talking about a very lucky person.
          
        * (lema, type, sense) triplet is equivalent to wordnet sysnsets
        
        * the different synonyms could be equivalent to wordnet lemmas 
            (lema, type, sense, synonym)
        
    """
    

    TYPENOUN = "noun"
    TYPEVERB = "verb"
    
    def __init__ (self):
        self.lema = None
        self.type = None
        self.sense = 1
        self.synonyms = []
        self.hypernyms = []
        self.hyponyms = []
        self.partMeronyms = []
        self.partHolynyms = []
        self.derivated = []
    
    def getLema(self):
        return self.lema
    
    def getType(self):
        return self.type
    
    def getSense(self):
        return self.sense
    
    def getSynonyms(self):
        return self.synonyms
        
    def getHypernyms(self):
        return self.hypernyms
    
    def getHyponyms(self):
        return self.hyponyms
    
    def getPartMeronyms(self):
        return self.partMeronyms
    
    def getPartHolonyms(self):
        return self.partHolynyms
    
    def getDerivated(self):
        return self.derivated
    
    def setLema(self, lema):
        self.lema = lema
        
    def setType(self, type):
        self.type = type
        
    def setSense(self, sense):
        self.sense = sense
        
    def setSynonyms(self, synonyms):
        self.synonyms = synonyms
   
    
    def setHypernyms(self, hypernyms):
        self.hypernyms = hypernyms
    
    def setHyponyms(self, semanticWorditem):
        self.hyponyms.append(semanticWorditem) 
    
    def setPartMeronyms(self, semanticWorditem):
        self.partMeronyms.append(semanticWorditem)
        
    def setPartHolonyms(self, semanticWorditem):
        self.partHolynyms.append(semanticWorditem)
    
    def setDerivated(self, derivated):
        self.derivated = derivated
    
    def appendSynonyms(self, moreSynonyms):
        
        for synonym in moreSynonyms:
            if not synonym in self.synonyms:
                self.synonyms.append(str(synonym))
        
    
    def __showHyponymInfo(self, father = ""):
        print "Lema ", self.getLema(), " Synonyms " , self.getSynonyms(), " father ", father 
        
    def showHyponyms(self, level = 1, father = ""):
        
        print "=========== Level  ", level , " =================="
        self.__showHyponymInfo( father )
        
        hyps = self.getHyponyms()
           
        if len(hyps) == 0:
            return
            
        for hyp in hyps:
            hyp.showHyponyms(level + 1, self.getLema())
        
    
    def compareSynonyms(self, semanticWord):
#    
#       When compare Synonyms, you have to consider that synonyms are related
#       to a word type (noun, verb) and sense. So, it is important to compare the 
#       synonyms, types and senses of a word.
#
#       But, If the semanticWordItem was created without type information (every 
#       semanticWordItem will have always a sense attribute), the synonyms
#       will be compared without worried about type and senses. This comparative
#       will not consider contextual information (sense and type)
#            
#    
   
        synonyms1 = self.getSynonyms()
        synonyms2 = semanticWord.getSynonyms()
        
        matchSynonyms = []
        
        for synonym1 in synonyms1:
            if synonym1 in synonyms2:
                matchSynonyms.append(synonym1)
        
        return matchSynonyms
    
    
    def __compareLemaAndHyponyms(self, semanticWords, lema, sense, type = None):
        
        for semanticWord in semanticWords:
            lemaC = [semanticWord.getLema()]
            lemaC.extend( semanticWord.getSynonyms())
            typeC = semanticWord.getType()
            senseC = semanticWord.getSense()
            
            if lema in lemaC  and sense == senseC:
                if type is None:
                    print "\t success ", lema , " in ", lemaC
                    return True
                else:
                    if ( (type == SemanticWordItem.TYPENOUN and typeC == SemanticWordItem.TYPENOUN) or 
                         (type == SemanticWordItem.TYPEVERB and typeC == SemanticWordItem.TYPEVERB) ):
                        print "\t success ", lema , " in ", lemaC
                        return True
            
        return False
    
    def __compareHyponyms(self, semanticWords, lema, sense, type = None, level = 1): 
        
        if len (semanticWords) > 0:
            if self.__compareLemaAndHyponyms (semanticWords, lema, sense, type ):
                return level
            else:
                for semanticWord in semanticWords:
                    semanticWordsDownLevel = semanticWord.getHyponyms()
                    
                    result = self.__compareHyponyms (semanticWordsDownLevel, lema, sense, type, level + 1)
                        
                    if result > 0:
                        return result
                return 0
        else:
            return 0
    
    def __equal__(self, semanticWord):
 
        if self.getLema() == semanticWord.getLema()  and self.getSense() == semanticWord.getSense():
                                                           
                if self.type is None or semanticWord.getType():
                    print "\t success ", self.getLema() , " in ", semanticWord.getLema()
                    return True
                else:
                    if ( (self.getType() == SemanticWordItem.TYPENOUN and semanticWord.getType() == SemanticWordItem.TYPENOUN) or 
                         (self.getType() == SemanticWordItem.TYPEVERB and semanticWord.getType() == SemanticWordItem.TYPEVERB) ):
                        print "\t success ", self.getLema() , " in ", semanticWord.getLema()
                        return True
        return False
        
    def __compareSameLevelHyponyms(self, hyps1, hyps2):
        
        for hyp1 in hyps1:
            for hyp2 in hyps2:
                if hyp1.__equal__(hyp2):
                    return True
        
        return False
    
    def compareSameLevelHyponyms(self, hyps1, hyps2, level = 1):
        
        
        if len(hyps1) > 0 and len(hyps2) > 0:
            if self.__compareSameLevelHyponyms(hyps1, hyps2):
                return level
            else:
                hyp1DownLevel = []
                for hyp1 in hyps1:
                    hyp1DownLevel.extend (hyp1.getHyponyms()) 
                    
                hyp2DownLevel = []
                for hyp2 in hyps2:
                    hyp2DownLevel.extend (hyp2.getHyponyms())
                
                result = self.compareSameLevelHyponyms(hyp1DownLevel, hyp2DownLevel, level + 1) 
                
                if result > 0:
                    return result
                return 0
        else:
            return 0
    ##
    # compare hyponyms values of both words:
    #    * the hyponyms of word1 against hyponyms of word2
    #    * the lema/sense/type of word1 against the hyponyms of word 2
    #    * the lema/sense/type of word2 against the hyponyms of word 1
    # This function compare all the levels of the hyponyms tree
    #
    # @param semanticWord: the word to compare
    # @param importantWord: if one of the word is marked as more important, 
    # then, this word is not compared against the other word meronyms
    # @return: the level of depth, where the function has succeded 
    ##  
    def compareHyponyms(self, semanticWord,  importantWord = None):
        
        hyponyms1 = self.getHyponyms()
        hyponyms2 = semanticWord.getHyponyms()
        
        lema1 = self.getLema()
        type1 = self.getType()
        sense1 = self.getSense()
        
        lema2 = semanticWord.getLema()
        type2 = semanticWord.getType()
        sense2 = semanticWord.getSense()

        if importantWord is None:
            levelSuccess = self.compareSameLevelHyponyms(hyponyms1, hyponyms2, 1)
            if  levelSuccess > 0:
                return levelSuccess

        if importantWord is None or importantWord == 1:
            levelSuccess = self.__compareHyponyms (hyponyms1, lema2, sense2, type2)
            if levelSuccess > 0:
                return levelSuccess
        if importantWord is None or importantWord == 2:
            levelSuccess = self.__compareHyponyms (hyponyms2, lema1, sense1, type1 )
            if  levelSuccess > 0:
                return levelSuccess

        
        return 0
        
        
        pass
    
    ##
    # compare meronyms values of both words:
    #    * the meronyms of word1 against meronyms of word2
    #    * the lema/sense/type of word1 against the meronyms of word 2
    #    * the lema/sense/type of word2 against the meronyms of word 1
    #
    # @param semanticWord: the word to compare
    # @param importantWord: if one of the word is marked as more important, 
    # then, this word is not compared against the other word meronyms
    # @return: True if one of the meronyms appears in the other word 
    #    information
    def comparePartMeronyms(self, semanticWord, importantWord = None):
        
        partMeronyms1 = self.getPartMeronyms()
        partMeronyms2 = semanticWord.getPartMeronyms()
        
        lema1 = self.getLema()
        type1 = self.getType()
        sense1 = self.getSense()
        
        lema2 = semanticWord.getLema()
        type2 = semanticWord.getType()
        sense2 = semanticWord.getSense()
        
        
        
        #compare meronyms of the same level
        if importantWord is None:
            for partMeronym1 in partMeronyms1:
                for partMeronym2 in partMeronyms2:
                    if partMeronym1.__equal__(partMeronym2):
                        return True
                    
        
        # compare the first level lema of a word
        # against the meronyms of the other word
        # if need it 
         
        if importantWord is None or importantWord == 1:
            for partMeronym1 in partMeronyms1:
                if semanticWord.__equal__(partMeronym1):
                    return True
        
        if importantWord is None or importantWord == 2:
            for partMeronym2 in partMeronyms2:
                if self.__equal__(partMeronym2):
                    return True
            
        return False
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    