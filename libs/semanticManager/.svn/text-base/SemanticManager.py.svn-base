
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


import os
import sys

import SemanticManagerSettings

from Relations.WordRelation import *
from StringSemanticTokenizer import StringSemanticTokenizer  
from SemanticManagerUtils import SemanticManagerUtils

from TimeDebug import TimeDebug


class SemanticManager:

    corpusPath = SemanticManagerSettings.CORPUSPATH 
    semanticManagarSimilarityMax = 6666
    pathValueMAX = 1
    lchValueMAX = 3.63758615973 # I have to test that max value returned is 3.63758615973

    LOG = False
    DEBUG = False
    DEBUGTIME = False
    COUNT = 0
    
    listSuccess = []
    listFails = []
    
    def configure(self):
        self.engine = WordnetSearchEngine()
        self.engine.configure(self.corpusPath)
        self.semanticUtils = SemanticManagerUtils()
        
        self.relationsManager = WordRelation(self.engine)
        
        self.lema = None
        self.depthHyponyms = 1
        self.sense = 1
        self.searchAlgLevel = SemanticManagerSettings.SEARCH_ALG_LEVEL
                
        if self.LOG:
            if not os.path.isdir("./similar"):
                os.mkdir("./similar")

    def __addSuccess(self, successInfo):
        self.listSuccess.append(successInfo)
        
    def __addFail(self, FailInfo):
        self.listFails.append(FailInfo)

            
    def __showSuccessFailResume(self):
        print "Fail list ", self.listFails
        print "Success List", self.listSuccess
        
        v1F = 0
        v2F = 0
        v3F = 0
        
        for fail in self.listFails:
            if v1F < fail[0]:
                v1F = fail[0]
            if v2F < fail[1]:
                v2F = fail[1]
            if v3F < fail[2]:
                v3F = fail[2]
        
        v1S = 666
        v2S = 666
        v3S = 666
        
        for success in self.listSuccess:
            if v1S > success[0]:
                v1S = success[0]
            if v2S > success[1]:
                v2S = success[1]
            if v3S > success[2]:
                v3S = success[2]
        
        v1SS = 666
        v2SS = 666
        v3SS = 666
        
        # search for the smaller success index BUT greater than 
        # the biggest fail index. Ex: if the biggest index for v1 is
        # 0.5 v1S could be 0.3, but the important result is v1SS that should be
        # at least 0.51, so we are going to search the smaller number above v1F
        for success in self.listSuccess:
            if v1SS > success[0] and success[0] > v1F:
                v1SS = success[0]
            if v2SS > success[1] and success[0] > v3F:
                v2SS = success[1]
            if v3SS > success[2] and success[0] > v3F:
                v3SS = success[2]
        
        if v1SS == 666:
            v1SS = v1F
        
        if v2SS == 666:
            v2SS = v2F
            
        if v3SS == 666:
            v3SS = v3F
        
        print "Biggest index failed:"
        print "\t", v1F
        print "\t", v2F
        print "\t", v3F
        
        print "Smaller index succeeded:"
        print "\t", v1S
        print "\t", v2S
        print "\t", v3S
    
        print "Smaller index succedded above the biggest respectively"
        print "\t", v1SS
        print "\t", v2SS
        print "\t", v3SS
                
    
    def __similaritySimpleAlgorith(self, pathValue, lchValue, wupValue):
        
        if pathValue >= 0 :
            pathValuePercent = pathValue * 100
        else:
            pathValuePercent = 0
            
        if lchValue >= 0 :
            lchValuePercent = (lchValue * 100) / self.lchValueMAX
        else: 
            lchValuePercent = 0
            
        if wupValue >= 0:
            wupValuePercent = wupValue * 100
        else:
            wupValuePercent = 0
        
        return (pathValuePercent + lchValuePercent + wupValuePercent) / 3
    
    def __applySimilarityValuesAlgorith(self, pathValue, lchValue, wupValue):
        
        return self.__similaritySimpleAlgorith(pathValue, lchValue, wupValue) 
       
    def __similaritySemanticdWords(self, word1, word2, importantWord = None):
        
        if self.DEBUGTIME:
            similarityMeasure = TimeDebug()
            similarityMeasure.setStart()
            timeMeasure = TimeDebug()
        
        w1Synset = self.engine.synset(word1.getLema(), word1.getSense() , word1.getType() )
        w2Synset = self.engine.synset(word2.getLema(), word2.getSense() , word2.getType() )
        
        if word1.getLema() == word2.getLema:
            return self.semanticManagarSimilarityMax
        
        if self.DEBUGTIME:
            timeMeasure.setStart()
        v1 = self.engine.pathSimilarity(w1Synset, w2Synset)
        
        if self.DEBUGTIME:
            timeMeasure.setStop()
            print "\t\t\t __similaritySemanticdWords(): calculate pathSimilarity ", timeMeasure.interval()
            timeMeasure.setStart()
        
        if self.searchAlgLevel == 2:
            v2 = self.engine.lchSimilarity(w1Synset, w2Synset)

            if self.DEBUGTIME:
                timeMeasure.setStop()
                print "\t\t\t __similaritySemanticdWords(): calculate lchSimilarity ", timeMeasure.interval()
                timeMeasure.setStart()
            
            v3 = self.engine.wupSimilarity(w1Synset, w2Synset)  # return value between -1 -> 1

            if self.DEBUGTIME:
                timeMeasure.setStop()
                print "\t\t\t __similaritySemanticdWords(): calculate wupSimilarity ", timeMeasure.interval()
                timeMeasure.setStart()
        else:
            v2 = 0
            v3 = 0

        v4 = word1.compareSynonyms(word2)
        if self.DEBUGTIME:
            timeMeasure.setStop()
            print "\t\t\t __similaritySemanticdWords(): compare synonyms ", timeMeasure.interval()
            timeMeasure.setStart()
        
        v5 = word1.compareHyponyms(word2, importantWord)
        if self.DEBUGTIME:
            timeMeasure.setStop()
            print "\t\t\t __similaritySemanticdWords(): compare hyponyms ", timeMeasure.interval()
            timeMeasure.setStart()
        
        v6 = word1.comparePartMeronyms(word2, importantWord)
        if self.DEBUGTIME:
            timeMeasure.setStop()
            print "\t\t\t __similaritySemanticdWords(): compare part meronys ", timeMeasure.interval()
            timeMeasure.setStart()
        
        if self.LOG:
        #if self.DEBUG:
            print "=========================="
            print "(", word1.getLema(), ",", word2.getLema(), ")"
            print "\t PathSimilarity " , v1
            print "\t lchSimilarity ", v2
            print "\t wupSimilarity ", v3
            print "\t\t synonymous ", syn1 , " - " , syn2
            print "\t\t\t match ", v4 
            print "\t\t hyponyms "
            print "\t\t\t match level ", v5
            print "\t\t part meronyms "
            print "\t\t\t match level ", v6
            print "=========================="
            if self.DEBUG or v5 or v6:
                #option = raw_input("Press (1)True (2)False (E) Exit")
                option = "1"
                if option == "1":
                    self.__addSuccess((v1,v2,v3))
                elif option == "2":
                    self.__addFail((v1,v2,v3))
                elif option == "E" or option == "e":
                     self.__showSuccessFailResume()
                     exit(0)
                else:
                     self.__addFail((v1,v2,v3))
             
        if (v5 > 0):
            hypPercent = 50 / v5
        else:
            hypPercent = 0
            
        if (v6 > 0):
            partMeronymPercent = 50 / v6
        else:
            partMeronymPercent = 0
        
        if self.searchAlgLevel == 2:
            similarityPercent = self.__applySimilarityValuesAlgorith(v1, v2, v3) + (50 * len(v4) + (hypPercent) + (partMeronymPercent) )
        else:
            similarityPercent = (v1 * 100) + (50 * len(v4) + (hypPercent) + (partMeronymPercent) )
            
        
        #if v1 > 0.2  and v2 > 1.0 :
         #   print word1.getLema() , "-" , word2.getLema(), "\t", v1 , v2
        
        if self.DEBUGTIME:
            similarityMeasure.setStop()
            print "\t\t __similaritySemanticdWords(): ", similarityMeasure.interval()
        
        return similarityPercent
   
    def __similarityWords(self, word1, word2, type = None, importantWord = None):
        if self.DEBUGTIME:
            similarityWords = TimeDebug()
            
        if not isinstance(word1, SemanticWordItem):
            if self.DEBUGTIME:
                similarityWords.setStart()
            self.relationsManager.setLema(word1)
            self.relationsManager.setType(type)
            self.relationsManager.setDepthHyponyms(self.depthHyponyms)
            wordSemantic1 = self.relationsManager.start()
            if self.DEBUGTIME:
                similarityWords.setStop()
                print "\t__similarityWords(): create semantic word ", similarityWords.interval()
        else:
            wordSemantic1 = word1
        
        if wordSemantic1 is None:
            return None
        
        if not isinstance(word2, SemanticWordItem):
            if self.DEBUGTIME:
                similarityWords.setStart()
            self.relationsManager.setLema(word2)
            self.relationsManager.setType(type)
            self.relationsManager.setDepthHyponyms(self.depthHyponyms)
            wordSemantic2 = self.relationsManager.start()
            if self.DEBUGTIME:
                similarityWords.setStop()
                print "\t__similarityWords(): create semantic word ", similarityWords.interval()
        else:
            wordSemantic2 = word2
         
        if wordSemantic2 is None:
            return None
        
        return self.__similaritySemanticdWords(wordSemantic1, wordSemantic2, importantWord)

    def __serializeSentences(self, sentences):
        # we only want to analyze words and categories without worried 
        # about the sentence where appears
        
        result = []
        
        for sentence in sentences:
            for word in sentence:
                result.append(word)
            
        return result
    
    
    def __compareListOfWords(self, words1, words2, type = None, importantWord = None):
      
        result = []
        for word1 in words1:
            for word2 in words2:
                similarity = self.__similarityWords(word1[0], word2[0], type, importantWord)
                if similarity is not None:
                    result.append( ( word1[0] , word2[0] , similarity ) )
                            
        return result
    
    ##
    # Compare two string words in order to know how similarity are the words
    #
    # @param word1: string word to compare
    # @param word2: string word to compare
    # @return: percent level of similarity
    ##
    def compareWords(self, word1, word2):
        # returns how similarity are two words 
        # word1 and word2 are string words
        
        return self.__similarityWords(word1, word2)
    
    ##
    # Compare two SemanticWordItem objects in order to know how similarity are the words
    #
    # @param word1: SemanticWordItem object to compare
    # @param word2: SemanticWordItem object to compare
    # @return: percent level of similarity
    ##
    def compareSemanticWords(self, word1,word2):
        # returns how similarity are two words 
        # word1 and word2 are SemanticWordItem objects
        
        return self.__similaritySemanticdWords(word1, word2)

    ##
    #
    # Analyze the result of words, paragraph, sentences that have been
    # previously compared with a result of triplets (word1,word2,similarity). 
    # When similarity of a triplet is greater than similarityPercent
    # then this triplet has succeeded. When the percent of success is greater than successMathces
    # returns true
    #
    # @param wordCompared:  array of triplets about compared words (word1,word2,similarity)
    # @param similarityPercent: percent of similarity accepted 
    # @return: true if compared words are similar according a Simple comparative
    ##
    def analyzeWordComparedSimple(self, wordsCompared, similarityPercent = 40, successMatches = 5):
        
        nwords = len (wordsCompared) 
        
        if nwords < 1:
            return
        
        nSuccess = 0
        
        wordsSuccess = []
        for wordValue in wordsCompared:
            if wordValue[2] > similarityPercent:
                nSuccess = + nSuccess + 1
                wordsSuccess.append(wordValue)
        
        if nSuccess > 0 :
            successPercent = (nSuccess * 100) / nwords
        else:
            successPercent = 0
        
        if self.LOG:    
            print "Nouns compared " , nwords , " succeeded" , nSuccess , "(" , successPercent , "%)"
  
        if successPercent > successMatches:
            return True
        else:
            return False
    
    ##
    #
    # Analyze the result of words, paragraph, sentences that have been
    # previously compared with a result of triplets (word1,word2,similarity). 
    # Returns the triplet with greater value of similarity
    #
    # @param wordCompared:  array of triplets about compared words (word1,word2,similarity)
    # @param similarityPercent: percent of similarity accepted 
    # @return: Returns the triplet with greater value of similarity
    ##
    def betterValueWordCompared(self, wordsCompared, similarityPercent = 40):
        nwords = len (wordsCompared) 
        nSuccess = 0
        
        maxValue = similarityPercent
        betterTriplet = None
        
        for wordValue in wordsCompared:
            if wordValue[2] > maxValue:
                maxValue = wordValue[2]
                betterTriplet = wordValue
                
        
        return betterTriplet
        
        
    ##
    # Compare two string paragraphs in order to know how similarity are his words.
    # The function will extract sentences and nouns and verbs of these sentences
    # in order to compare the similarity. A paragraph could be only one sentence
    #
    # @param parag1: string paragraph to compare
    # @param parag2: string paragraph to compare
    # @return: array of triplets about compared words (word1,word2,similarity)
    ##          
    def compareParagraphs(self, parag1, parag2):
        # returns how similarity are two paragraphs 
        # parag1 and parag2 are string paragraphs
        
        stringTokenizer = StringSemanticTokenizer()
        sentences1 = stringTokenizer.analyzeParagraph(parag1)
        sentences2 = stringTokenizer.analyzeParagraph(parag2)
        
        
        words1 = self.__serializeSentences(sentences1)
        words2 = self.__serializeSentences(sentences2)
        
        
        nouns1 = self.semanticUtils.extractNouns(words1)
        vbs1 = self.semanticUtils.extractVB(words1)
        nouns2 = self.semanticUtils.extractNouns(words2)
        vbs2 = self.semanticUtils.extractVB(words2)
       
        wordsCompared = self.__compareListOfWords(nouns1, nouns2, SemanticWordItem.TYPENOUN)
        wordsCompared.extend( self.__compareListOfWords(vbs1, vbs2, SemanticWordItem.TYPEVERB) )

        return wordsCompared
          
    

    ##
    # Compare a string word against a paragraph in order to know how similarity are his words.
    # The function will extract sentences and nouns and verbs of these sentences
    # in order to compare the similarity. A paragraph could be only one sentence
    #
    # @param word: string word or semantic word to compare
    # @param parag: string paragraph to compare
    # @param wordType: the 'word' type. when None, compareWordParagraph will try to
    #     determine the type
    # @param importantWord: if one of the word is marked as more important, 
    #     then, this word is not compared against the other word meronyms
    # @return: array of triplets about compared words (word1,word2,similarity)
    ##          
    def compareWordParagraph(self, word, parag, wordType = None, importantWord = None ):
    
        if self.DEBUGTIME:
            compareWord = TimeDebug()
            
        stringTokenizer = StringSemanticTokenizer()
        
        if self.DEBUGTIME:
            compareWord.setStart()
            
        sentencesTagged = stringTokenizer.analyzeParagraph(parag)
        if self.DEBUGTIME:
            compareWord.setStop()
            print "\tcompareWordParagraph(): analyzeParagraph in ", compareWord.interval()
            compareWord.setStart()
            
        wordsTaggedP = self.__serializeSentences(sentencesTagged)
        if self.DEBUGTIME:
            compareWord.setStop()
            print "\tcompareWordParagraph(): serialize sentences in ", compareWord.interval()
            compareWord.setStart()
        
        
        nouns1 = []
        vbs1 = []
       
        nouns2 = self.semanticUtils.extractNouns(wordsTaggedP)
        vbs2 = self.semanticUtils.extractVB(wordsTaggedP)
        
        if len(nouns2) == 0 and len(vbs2) == 0:
            return []
        
        if not isinstance(word, SemanticWordItem):
            if wordType == None:
                wordTagged = stringTokenizer.analyzeWord(word)
                if ( len(wordTagged) == 0 or 
                     ( not self.semanticUtils.isNoun(wordTagged) and not self.semanticUtils.isVB(wordTagged) ) ):
                    print "The word \"", word , "\" with a no type allowed (noun or verb)"
                    return []
            else:
                if wordType == SemanticWordItem.TYPENOUN:
                    nouns1 = [[word, 'N']]
                elif wordType == SemanticWordItem.TYPEVERB:
                    vbs1 = [[word, 'V']]
                else:
                    print "The word ", word , " with a no type allowed (noun or verb)"
                    return []
        else:
            type = word.getType()
            if type == SemanticWordItem.TYPENOUN or type == None:
                nouns1 = [[word, 'N']]
            elif type == SemanticWordItem.TYPEVERB:
                vbs1 = [[word, 'V']]
            else:
                print "The word ", word.getLema() , " with a no type allowed (noun or verb)"
                return []
                

        
        
        # nouns1 or vbs1 always only one word
        if len(nouns1) > 0:
            wordsCompared = self.__compareListOfWords(nouns1, nouns2, SemanticWordItem.TYPENOUN, importantWord)
        else:
            wordsCompared = self.__compareListOfWords(vbs1, vbs2, SemanticWordItem.TYPEVERB, importantWord)
        
        return wordsCompared
      
        
       
        
    ##
    # Set the sense of the word to search
    #
    # @param sense: word sense 
    #
    ##
    def setSense(self, sense):
        self.sense = sense
        
        
    ##
    # Set the lema for search the different information allowed for the SemanticManager
    #
    # @param lema: lema string. Ex.: dog
    #
    ##
    def setLema(self, lema):
        self.lema = lema
    
    ##
    # Set the maximum depth of hyponyms tree
    #
    # @param depth: depth of hyponyms tree
    #
    ##  
    def setDepthHyponyms(self, depth):
        self.depthHyponyms = depth
        
        
    ##
    # Set the search algorithm level
    #
    # @param level:  1 good performance 2 better search results
    #    with better search results path algorithms are used during
    #    the similarity search
    #
    ##  
    def setSearchAlgLevel(self, level):
        self.searchAlgLevel = level
    
    ##
    # The SemanticManager starts to search the different informaiton and relations
    # according to the configuration. 
    # (Only Semantic Words Relations with Wordnet in this version)
    #
    # @return: a list of GenericItems related to the configured lema
    #
    ##      
    def start(self):
        if (self.lema is not None):
            self.relationsManager.setLema(self.lema)
            self.relationsManager.setSense(self.sense)
            self.relationsManager.setDepthHyponyms(self.depthHyponyms)
            wordSemantic = self.relationsManager.start()
            
            return wordSemantic
   
    def test(self):
        pass

        
        



if __name__ == "__main__":
    pass
   

