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
#  Author : Roberto Calvo Palomino <rocapal@gsyc.es>
#
#

from Items.PhotoItem import *

from GenericChannel import *

from urllib2 import urlopen
from xml.dom.minidom import parseString

import json

class PanoramioChannel (GenericChannel):

	url_api = "http://www.panoramio.com/map/get_panoramas.php?order=popularity&set=public&from=0&to=10&size=small&minx=%s&miny=%s&maxx=%s&maxy=%s"

	def __init__ (self, place):

		self.photo_list = []

	def set_config (self, pattern, latitude, longitude, radius):

		self.set_search_pattern (pattern)
		self.latitude = latitude
		self.longitude = longitude
		self.radius = radius


	def process (self):

		# got operations below from http://assets.en.oreilly.com/1/event/2/Geo%20Distance%20Search%20with%20MySQL%20Presentation.ppt
		# 1 miles = 1.609344 kilometers
		
		miny = float(self.latitude) - ( float(self.radius) / ( 69 * 1.609344 ) )
		maxy = float(self.latitude) + ( float(self.radius) / ( 69 * 1.609344 ) )

		# estos son los calculos correctos pero python da error en las funciones cos y radians
		#minx = float(longitud) - float(radio) / ( abs( cos( radians( float(latitud) ) * (69 * 1.609344) )))
		#maxx = float(longitud) + float(radio) / ( abs( cos( radians( float(latitud) ) * (69 * 1.609344) )))
		
		# chapuza para obtener un rango alrededor de la longitud dada
		minx = float(self.longitude) - ( float(self.radius) / ( 69 * 1.609344 ) * 1 )
		maxx = float(self.longitude) + ( float(self.radius) / ( 69 * 1.609344 ) * 1 )
		
		# la chapuza de arriba genera un rectangulo mas pequenyo de lo que deberia
		# python: latitud 40.333313 miny 40.3261086963 maxy 40.3405173037 longitud -3.87429 minx -3.88149430368 maxx -3.86708569632
		# perl: latitud 40.333313 longitud -3.87429 - minx -4.37429 maxx -3.33800323823823 - pi 3.14159265358979 - degrees 0.703949110087432
		# print "latitud %s miny %s maxy %s longitud %s minx %s maxx %s" % ( latitud, miny, maxy, longitud, minx, maxx )
		

		url_panoramio = self.url_api % ( minx, miny, maxx, maxy)


		response = urlopen(url_panoramio)
		spanoramio = response.read()
		feedpanoramio = json.JsonReader().read(spanoramio)


		for item in feedpanoramio["photos"]:

			photo = PhotoItem()

			photo.service = "Panoramio"

			photo.title = unicode(item["photo_title"], 'UTF-8')
			photo.date = unicode(item["upload_date"], 'UTF-8')
			photo.longitude = item["longitude"]
			photo.latitude = item["latitude"]
			photo.url_image = item["photo_file_url"]
			photo.url_thumb =  item["photo_file_url"].replace('/small/','/thumbnail/')
			photo.img_height = item["height"]
			photo.img_width = item["width"]
			photo.thumb_height =  int( int(item["height"]) / 2.4 )
			photo.thumb_width = int( int(item["width"]) / 2.4 )
			photo.credits_owner = unicode(item["owner_name"], 'UTF-8')
			photo.credits_url = item["owner_url"]
			photo.url = item["photo_url"]

			print photo.title + " - " + photo.service

			self.photo_list.append(photo)


		
			
