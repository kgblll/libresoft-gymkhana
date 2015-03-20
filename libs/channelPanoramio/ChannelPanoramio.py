#!/usr/bin/env python

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
#
#

from GIC.Channels.GenericChannel import *
from social.core.models import Photo, Person

from urllib2 import urlopen, HTTPError
from xml.dom.minidom import parseString

from Config import channel_icon_url, max_size_search, description
from django.contrib.gis.geos import Point

import simplejson
from StringIO import StringIO


 
class ChannelPanoramio (GenericChannel):

	MANDATORY_FIELDS = ["latitude", "longitude", "radius", "category"]
	CATEGORIES = [{"id" : "0", "name" : "all", "desc" : "All categories"}]
	
	url_api = "http://www.panoramio.com/map/get_panoramas.php?order=popularity&set=public&from=0&to=%d&size=small&minx=%s&miny=%s&maxx=%s&maxy=%s" 

	def __init__ (self):

		self.photo_list = []
		self.options = {}
	
	def _category_type(self):
		
		selected_category = self.options["category"]
		result = False
		
		for category in self.CATEGORIES:
			if selected_category == category["id"]:
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

		if self._category_type() == False:
			return False, "Category not supported"
		
		# got operations below from http://assets.en.oreilly.com/1/event/2/Geo%20Distance%20Search%20with%20MySQL%20Presentation.ppt
		# 1 miles = 1.609344 kilometers
		
		miny = float(self.options["latitude"]) - ( float(self.options["radius"]) / ( 69 * 1.609344 ) )
		maxy = float(self.options["latitude"]) + ( float(self.options["radius"]) / ( 69 * 1.609344 ) )

		# this should be the right parameters, but we have problems with python 
		#minx = float(longitud) - float(radio) / ( abs( cos( radians( float(latitud) ) * (69 * 1.609344) )))
		#maxx = float(longitud) + float(radio) / ( abs( cos( radians( float(latitud) ) * (69 * 1.609344) )))
		
		# fixe to solve the mathematic calculate problem, but the rectangle is minor than expected
		minx = float(self.options["longitude"]) - ( float(self.options["radius"]) / ( 69 * 1.609344 ) * 1 )
		maxx = float(self.options["longitude"]) + ( float(self.options["radius"]) / ( 69 * 1.609344 ) * 1 )
		
				# python: latitud 40.333313 miny 40.3261086963 maxy 40.3405173037 longitud -3.87429 minx -3.88149430368 maxx -3.86708569632
		# perl: latitud 40.333313 longitud -3.87429 - minx -4.37429 maxx -3.33800323823823 - pi 3.14159265358979 - degrees 0.703949110087432
		# print "latitud %s miny %s maxy %s longitud %s minx %s maxx %s" % ( latitud, miny, maxy, longitud, minx, maxx )
		

		url_panoramio = self.url_api % (max_size_search, minx, miny, maxx, maxy)

		try:
			response = urlopen(url_panoramio)
			spanoramio = response.read() 
			io = StringIO(spanoramio)
			feedpanoramio = simplejson.load(io,"UTF-8")
		except HTTPError, e:
			return (False, e )

		person = Person(pk = 666, position= Point(0.0, 0.0 , srid=4326)	)
		
		for item in feedpanoramio["photos"]:

			photo = Photo(pk = 666,
						name = item["photo_title"], 
					uploader = person, 
					description = "",
					photo_url = item["photo_file_url"].replace('/small/','/medium/'),
					photo_thumb_url = item["photo_file_url"],
					info_url = item["photo_url"],
					since = item["upload_date"],
					position =  Point(float(item["longitude"]), float(item["latitude"]), srid=4326),
					icon = channel_icon_url,
					type = "photo" ,
					altitude = None)
			
#			photo = Photo()
#
#			photo.name = item["photo_title"]
#			photo.description = ""
#			photo.photo_url = item["photo_file_url"].replace('/small/','/medium/')
#			photo.external_info["photo_thumb"] = item["photo_file_url"]
#			photo.external_info["photo_url"] = item["photo_file_url"].replace('/small/','/medium/')
#			photo.external_info["info_url"]= item["photo_url"]
#			photo.since = item["upload_date"]
#			photo.position = { "longitude" : item["longitude"],
#							   "latitude" : item["latitude"]}
#			
#			photo.icon = channel_icon_url
			
			self.photo_list.append(photo)

		return (True, self.photo_list)

		
			
