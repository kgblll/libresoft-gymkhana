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

class SemanticManagerUtils:

	def __init__(self):
		pass
 
 
	def isNoun(self, word):
	   if word.startswith("N") :
		  return True
	   else:
		  return False
	   
	def isVB(self, word):
	   if word.startswith("V") :
		  return True
	   else:
		  return False
	   
	def extractNouns(self, wordsList):
	   result = []
	   for word in wordsList:
		  if self.isNoun(word[1]):
			 result.append(word)
		  
	   return result

	def extractVB(self, wordsList):
	   result = []
	   
	   for word in wordsList:
		  if self.isVB(word[1]):
			 result.append(word)
		  
	   return result   