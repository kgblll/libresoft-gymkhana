
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

from SemanticManager import SemanticManager
from Relations.WordRelation import *

from xml.dom import minidom
from xml.dom.minidom import Document, parseString


p1 = "Music, At its core, the semantic web comprises a set of design principles, collaborative working groups, and a variety of enabling technologies. Some elements of the semantic web are expressed as prospective future possibilities that are yet to be implemented or realized. Other elements of the semantic web are expressed in formal specifications. Some of these include Resource Description Framework (RDF), a variety of data interchange formats (e.g. RDF/XML, N3, Turtle, N-Triples), and notations such as RDF Schema (RDFS) and the Web Ontology Language (OWL), all of which are intended to provide a formal description of concepts, terms, and relationships within a given knowledge domain."
p2 = "Heavy metal (often referred to simply as metal) is a genre of rock music that developed in the late 1960s and early 1970s, largely in England and the United States. With roots in blues-rock and psychedelic rock, the bands that created heavy metal developed a thick, massive sound, characterized by highly amplified distortion, extended guitar solos, emphatic beats, and overall loudness. Heavy metal lyrics and performance styles are generally associated with masculinity and machismo."
p3 = "Hard rock or heavy rock is a sub-genre of rock music which has its earliest roots in mid-1960s garage and psychedelic rock and is considerably harder than conventional rock music. It is typified by a heavy use of distorted electric guitars, bass guitar, drums, pianos, and other keyboards."
p4 = "Hard rock is strongly influenced by blues music; the most frequently used scale in hard rock is the pentatonic, which is a typical blues scale. Unlike traditional rock and roll (which takes elements of the old blues), hard rock incorporates elements of British blues, a style of blues played with more modern instruments such as electric guitars, drums, keyboards and electric bass. A notable departure from traditional blues forms is that hard rock is seldom restricted to the I, IV, and V chords prevalent in twelve or sixteen bar blues, but includes other chords, typically major chords rooted on tones of the minor scale."
 
 
def __unicodeStrim (str):
    return unicode.rstrip(unicode.lstrip(str))


def analyzeXML(fileName):
    
    conf = minidom.parse(fileName)
    photosXML = conf.getElementsByTagName("Photo");
    photosInfo = []
 
    for photo in photosXML:
        
        if photo.getElementsByTagName("title") != None:
            title = photo.getElementsByTagName("title")[0].firstChild.data
            
        if photo.getElementsByTagName("description") != None:
            description =photo.getElementsByTagName("description")[0].firstChild.data
            
        if photo.getElementsByTagName("url") != None:
            url = photo.getElementsByTagName("url")[0].firstChild.data
        
        if photo.getElementsByTagName("urlHtml") != None:
            urlHtml = photo.getElementsByTagName("urlHtml")[0].firstChild.data
            
        tags = []
        if photo.getElementsByTagName("tags") != None :
            tagsXML = photo.getElementsByTagName("tags")[0]
         
            if len(tagsXML.getElementsByTagName("tag")) != 0 :
                for tagXML in photo.getElementsByTagName("tag"):
                    tags.append( tagXML.firstChild.data )
                    
        photosInfo.append({'title':title, 'description':description, 'url':url, 'urlHtml':urlHtml, 'tags':tags})
                           
    return photosInfo
            
            
            
def testFlicker( compareWord ):
    photosInfo =  analyzeXML("./prueba.xml")
    
    
    semanticManager.setDepthHyponyms(1)
    semanticManager.setLema(compareWord)
    compare = semanticManager.start()
    
    #compare = "music"
    
    print len(photosInfo)
    a=1
    
    if DEBUGTIME:
        photoTime = TimeDebug()
        photoEntireTime = TimeDebug()
        
    resume = []
    for photo in photosInfo:
                    
        if DEBUGTIME:
            photoEntireTime.setStart()
            
        if photo['description'] != None and photo['description'] != "":
            
            if DEBUGTIME:
                photoTime.setStart()
                
            
            wordsCompared = semanticManager.compareWordParagraph(compare, photo['description'], SemanticWordItem.TYPENOUN, 1)
            
            if DEBUGTIME:
                photoTime.setStop()
                print "Flicker process(): compared words in ", photoTime.interval()
                photoTime.setStart()
                
            result = semanticManager.analyzeWordComparedSimple(wordsCompared)
            
            if DEBUGTIME:
                photoTime.setStop()
                print "Flicker process(): analyze result in ", photoTime.interval()
                photoTime.setStart()
            
            if result:
                betterValue = semanticManager.betterValueWordCompared(wordsCompared)
                if DEBUGTIME:
                    photoTime.setStop()
                    print "Flicker process(): extract better value in ", photoTime.interval()
                    photoTime.setStart()
                if LOG:
                    print photo['url']
                    print photo['urlHtml']
                    print "Look a description success: ", photo['description'], " better similarity ", betterValue
                #raw_input("")
                resume.append( [betterValue, ("Description", photo['url'], photo['urlHtml']) ])
                
                
        if photo['title'] != None and photo['title'] != "":
            
            if DEBUGTIME:
                photoTime.setStart()
                
            wordsCompared = semanticManager.compareWordParagraph(compare, photo['title'], SemanticWordItem.TYPENOUN, 1)
            
            if DEBUGTIME:
                photoTime.setStop()
                print "Flicker process(): compared words in ", photoTime.interval()
                photoTime.setStart()
                
            result = semanticManager.analyzeWordComparedSimple(wordsCompared)
            if DEBUGTIME:
                photoTime.setStop()
                print "Flicker process(): analyze result in ", photoTime.interval()
                photoTime.setStart()
                
            if result:
                betterValue = semanticManager.betterValueWordCompared(wordsCompared)
                if DEBUGTIME:
                    photoTime.setStop()
                    print "Flicker process(): extract better value in ", photoTime.interval()
                    photoTime.setStart()
                if LOG:
                    print photo['url']
                    print photo['urlHtml']
                    print "Look a title success: ", photo['title'] , " better similarity ", betterValue
                #raw_input("")
                resume.append( [betterValue, ("Title", photo['url'], photo['urlHtml'])])
        
        if photo['tags'] != None and len(photo['tags']) :
            if DEBUGTIME:
                photoTime.setStart()
            tagCounter = 0
            tagSuccess = []
            ntags = len (photo['tags'])
            for photoTag in photo['tags']:
                wordsCompared = semanticManager.compareWordParagraph(compare, photoTag, SemanticWordItem.TYPENOUN, 1)
                
                if DEBUGTIME:
                    photoTime.setStop()
                    print "Flicker process(): compared words in ", photoTime.interval()
                    photoTime.setStart()
                    
                result = semanticManager.analyzeWordComparedSimple(wordsCompared)
                
                if DEBUGTIME:
                    photoTime.setStop()
                    print "Flicker process(): analyze result in ", photoTime.interval()
                    photoTime.setStart()
                    
                if result:
                    betterValue = semanticManager.betterValueWordCompared(wordsCompared)
                    
                    if DEBUGTIME:
                        photoTime.setStop()
                        print "Flicker process(): extract better value in ", photoTime.interval()
                        photoTime.setStart()
                    
                    if LOG:
                        print photo['url']
                        print photo['urlHtml']
                        print "Look a tags success: ", tagSuccess , " better similarity ", betterValue
                    #raw_input("")
                    resume.append([betterValue, ("Tag", photo['url'], photo['urlHtml'])])
        
        if DEBUGTIME:
            photoEntireTime.setStop()
            print "Flicker process(): photo complete in ", photoEntireTime.interval()
            
        print "====photo ", a , " analyzed==== "
        
        a = a + 1
        if a > 200:
            break
        

            
        
        #show resume
    resumeOrdered = []
    
    while len (resume) > 0:
        maxInfo = 0
        index = 0
        i = 0
        for info in resume:
            if info[0][2] > maxInfo :
                maxInfo = info[0][2]
                index = i
            i = i + 1
        
        print "maxvalue ", maxInfo  
        resumeOrdered.append (resume[index])
        del resume[index]
    
        
    fileHandle = open ("./similarResults.txt", "w")
    save_stdout = sys.stdout
    sys.stdout = fileHandle
        
    
    for similar in resumeOrdered:
        print "========================"
        print " Words : " , similar[0][0].getLema(), " and " , similar[0][1], " with value ", similar[0][2]
        print " Type: ", similar[1][0]
        print " \t url ", similar[1][1]
        print " \t urlHTML ", similar[1][2]
            
        print "========================"
        
    fileHandle.close()
    sys.stdout = save_stdout 
        
def testmbox():
    
        
    mlAccessDirect = MLAccessDirect()
    emailList = mlAccessDirect.getAllMessages( "./", "test.mbox")
    emailList2 = mlAccessDirect.getAllMessages( "./", "test2.mbox")
       
    COUNT = 0
    word = "License"
    for email1 in emailList:
        body1 = email1['body']
        for email2 in emailList2:
            body2 = email2['body']
            wordsCompared = semanticManager.compareParagraphs( body1 , body2 )
            #wordsCompared = semanticManager.compareWordParagraph(word, body2)
            result = semanticManager.analyzeWordComparedSimple(wordsCompared)
                
            print "***", result , "***"
            if result == True:
                if LOG:
                    COUNT = COUNT + 1 
                    fileHandle = open ("./similar/similar." + str(COUNT) , 'w' )
                    save_stdout = sys.stdout
                    sys.stdout = fileHandle
                    
                print "=================================================================="
                print body1
                print "******************************************************************"
                print body2
                print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
                print wordsCompared
                print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
            
                if LOG:
                    fileHandle.close()
                    sys.stdout = save_stdout
    semanticManager.__showSuccessFailResume()
    
def test():
    
    #semanticManager.LOG = False

    #testFlicker("bird")
    #testmbox()

    semanticManager.setDepthHyponyms(2)
    
    semanticManager.setLema("music")
    semanticWord1 = semanticManager.start()
    
    print semanticWord1.getSynonyms()
    
    semanticManager.setLema("table")
    semanticWord1 = semanticManager.start()
    
    print semanticWord1.getSynonyms()
    
    semanticManager.setLema("parrot")
    semanticWord1 = semanticManager.start()
    
    print semanticWord1.getSynonyms()

    
   # semanticWord1.showHyponyms()
    
    
    
    
#
    #semanticManager.setLema("whelp")
    #semanticManager.setLema("europe")
    semanticManager.setLema("bird")
    semanticManager.setSense(1)
    semanticWord2 = semanticManager.start()
    print semanticWord2.getSynonyms()
    

    
    #semanticWord2.showHyponyms()
    
    #print semanticWord2.getHyponyms()
#    
    #print semanticWord1.getSynonyms()
    #print semanticWord2.getSynonyms()
#    
    
    print semanticManager.compareSemanticWords(semanticWord1, semanticWord2)
#    print semanticManager.compareWords("dog", "cat")
           

    
#    wordsCompared = semanticManager.compareWordParagraph("music", semanticManager.p1)
#    result =  semanticManager.analyzeWordComparedSimple(wordsCompared)
#    
#    print wordsCompared
#    print "***", result , "***"
 

LOG = False
DEBUGTIME = False



if __name__ == '__main__':
    semanticManager = SemanticManager()
    semanticManager.configure()
    semanticManager.setSearchAlgLevel(2)
    test()
    #import memory
    #print memory.mem("rsz")
    pass