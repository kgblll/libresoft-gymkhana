#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2009-2010 GSyC/LibreSoft, Universidad Rey Juan Carlos
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
#			Jose Gato Luis <jgato@libresoft.es>
#
#


from social.core.models import Person, Note
from GIC.Channels.GenericChannel import *

from urllib2 import urlopen, HTTPError
from xml.dom.minidom import parseString

from Config import channel_icon_url, max_size_search, description
from django.contrib.gis.geos import Point
#import sys
#sys.path.insert (0, "../GoogleApi")
#from GoogleApi.GoogleTranslate import *

class Channel11870 (GenericChannel):

	MANDATORY_FIELDS = ["latitude", "longitude", "radius", "category"]
	
	CATEGORIES = [{"id" : "0", "name" : "all", "desc" : "All supported categories in 11870"},
				  {"id" : "1", "name" : "restaurantes", "desc" : "Restaurants"},
				  {"id" : "2", "name" : "compras", "desc" : "Places for shopping"},
				  {"id" : "3", "name" : "noche-discotecas", "desc" : "Pubs, discos..."},
				  {"id" : "4", "name" : "casas-rurales-montana", "desc": "Houses in the mountain"}]
	
	url_api = "http://11870.com/api/v1/search?authSign=3572a8bb3f7dc6c9b2b80907beff2f5f&appToken=74805753bf8cef647b46101266370e05&"
	url_11870 = " "

	def __init__ (self):
		self.places_list = []
		self.options = {}
		
	def _category_type(self):
		
		selected_category = self.options["category"]
		result = False
		
		for category in self.CATEGORIES:
			if selected_category == category["id"]:
				if category["id"] == 0:
					result = ""
				else:
					result = category["name"]
				break;
		
		return result
	
	def get_categories(self):
		return self.CATEGORIES	
		
	def get_info(self):
		return description
	
	def set_mandatory_fields(self, dict):
	
		for field in self.MANDATORY_FIELDS:
			if not field in dict:
				return (False, field)
			else:
				self.options[field] = dict[field]
		  
		return (True, "")
	
	def set_options(self, options):
		
		success, result = self.set_mandatory_fields(options)
	
		if not success:
			return False, "\"%s\" parameter is mandatory " % (result)
		
		return True, ""

	def process (self):
		
		category = self._category_type()
		
		if category != False:
			url11870 = self.url_api + "count=%s&lat=%s&lon=%s&radius=%s&q=%s&category=%s" % (max_size_search, self.options["latitude"], self.options["longitude"], self.options["radius"], self.search_pattern, category )
		else:
			return (False, "Category not supported")

		try:
			r = urlopen( url11870 )
			string_data = r.read()
			dom = parseString(string_data)
			feed = dom.firstChild
			resp = feed.toxml();
		except HTTPError, e:
			return (False, e )


		person = Person(pk = 666, position= Point(0.0, 0.0 , srid=4326)	)
	
		
		for item in feed.getElementsByTagName("entry"):
			
			place = Note(pk = 666,
						title = self.getInnerText(item, "title"),
						text = self.getInnerText(item, "summary"),
						icon = channel_icon_url,
						uploader = person,
						type = "note",
						altitude = None) 

			pos = self.getInnerText(item, "gml:pos")
			
			try:
				latitude = pos.split(' ')[0]
				longitude = pos.split(' ')[1] 
								
				place.position =  Point( float(longitude), float(latitude),  srid=4326)
				 
			except ValueError:
				print ValueError
				place.position =  Point( 0.0, 0.0, srid=4326) 
 
 			
			print place.get_dictionary() 
			self.places_list.append (place)

		return (True, self.places_list)
			
	def getInnerText (self, domNode, tag=None):
		try:
			if tag ==None:
				return domNode.childNodes[0].nodeValue
			else:
				return domNode.getElementsByTagName(tag)[0].childNodes[0].nodeValue
		except:
			return None
			
