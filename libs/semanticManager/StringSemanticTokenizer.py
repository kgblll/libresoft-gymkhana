#!/usr/bin/python
# -*- coding: utf-8 -*-
#
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
#  Author : Javier Pueyo   <jpueyo@libresoft.es>
#

import nltk.corpus, nltk.tag
import SemanticManagerSettings

from nltk.corpus import wordnet as my_wordnet

class StringSemanticTokenizer:
    

    def __init__(self):
        nltk.data.path.append (SemanticManagerSettings.CORPUSPATH)
        self.stop_words = nltk.corpus.stopwords.words('english')
        pass
        
    def __extractSentences (self, paragraph):
        return nltk.sent_tokenize(paragraph)

    def __extractWords (self, sentence):
        return nltk.word_tokenize(sentence)
   
    def __sentenceNounsVerbs(self, sentence):
        # return an array of tuples
        # first position of tuple is the lemma
        # and the second position the category
        # only nouns and verbs are returned
        
        pos_tags = nltk.pos_tag(sentence)
        result = []
   
        for pos_tag in pos_tags:
            if ( ( pos_tag[1].startswith("V") or pos_tag[1].startswith("N") ) and pos_tag[0] not in self.stop_words ):
                result.append((pos_tag[0] , pos_tag[1]))
        
        return result
    
    def analyzeWord (self, wordString):
       
        return self.analyzeSentence(wordString)
        
    def analyzeSentence(self, sentenceString):
        
        wordsSentence = self.__extractWords(sentenceString)
        return self.__sentenceNounsVerbs (wordsSentence)
        
        
    def analyzeParagraph(self, paragraphString):
        
        sentences = self.__extractSentences(paragraphString)
        
        result = []
        for sentence in sentences:
            wordsSentence = self.__extractWords(sentence)
            result.append( self.__sentenceNounsVerbs (wordsSentence))
        
        return result
        
#
#stringTokenizer = StringSemanticTokenizer()
#
#paragraph = "John had a little dog at home. I used to like him."
#
#sentences = stringTokenizer.extractSentences(paragraph)
#
#print sentences
#
#for sentence in sentences:
#    print sentence
#    words = stringTokenizer.extractWords( sentence)
#    print words

#nltk.data.path.append ("/home/jgato/proyectos/wordnet/corpus/")
#
## Le pasamos el párrafo que queremos analizar
#parrafo = "John had a little dog at home. I used to like him."
##parrafo = "I went to the bank for money."
##parrafo = "I bank in the Santander"
#
#stringSemanticTokenizer = StringSemanticTokenizer()
#
#print stringSemanticTokenizer.analyzeParagraph(parrafo)

#sentences = stringSemanticTokenizer.__extractSentences(parrafo)
#
#tok_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
#
#stringSemanticTokenizer.__sentenceNounsVerbs(tok_sentences[0])

## Dividimos el párrafo en frases (sentence tokenization)
#sentences = nltk.sent_tokenize(parrafo)
#
## Dividimos cada frase en palabras (word tokenization)
#tok_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
#
#print tok_sentences
#
#for pos_sentence in tok_sentences: 
#    print nltk.pos_tag(pos_sentence) 

# Asignamos la categoría gramatical a cada palabra (PoS tagging / aqui está la mayor dificultad porque según el tipo de lenguaje que le pases lo hará mejor o peor)


