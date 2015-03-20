#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
#  Author : Roberto Calvo Palomino <rocapal@gsyc.es>
#



from urllib2 import urlopen
from urllib import urlencode

import simplejson
import sys

# the google translate API can be found here:
# http://code.google.com/apis/ajaxlanguage/documentation/#Examples


class GoogleTranslate ():


	base_url = 'http://ajax.googleapis.com/ajax/services/language/translate?'
	orig_lang = ' '
	dest_lang = ' '

	def __init__ (self):
		# By default, the translate is between spanish and english
		self.orig_lang = 'es'
		self.dest_lang = 'en'

	
	def set_languages (self, orig_lang, dest_lang):
		""" 
		If orig_lang = "" Google tries to guess the
		orig language.
		"""
		self.orig_lang = orig_lang
		self.dest_lang = dest_lang

	def translate (self, text):

		self.text = text

		if len(text):
			lang_par = '%s|%s' % (self.orig_lang, self.dest_lang)
			
			params = urlencode( (('v',1.0),
								('q',self.text),
								('langpair',lang_par),) )
	
	
			resp = simplejson.load(urlopen('%s' % (self.base_url), data = params ))
			try:
				translation = resp['responseData']['translatedText']
			except:
				raise
		else:
			translation = ""													

		return translation
